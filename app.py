from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'postgresql.thoughts-app.svc.cluster.local',
    'database': 'thoughts',
    'user': 'thoughts',
    'password': 'thoughts123'
}

def get_db_connection():
    """Create and return a database connection"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def get_thoughts_with_stats(status_filter=None):
    """Fetch all thoughts with their latest evaluation data"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
        SELECT 
            t.id,
            t.content,
            t.author,
            t.author_bio,
            t.status,
            t.thumbs_up,
            t.thumbs_down,
            (t.thumbs_up - t.thumbs_down) as net_rating,
            t.created_at,
            t.updated_at,
            te.similarity_score,
            te.evaluated_at
        FROM thoughts t
        LEFT JOIN (
            SELECT DISTINCT ON (thought_id) 
                thought_id, 
                similarity_score, 
                evaluated_at
            FROM thought_evaluations
            ORDER BY thought_id, evaluated_at DESC
        ) te ON t.id = te.thought_id
    """
    
    # Add status filter if provided
    if status_filter and status_filter != 'ALL':
        query += " WHERE t.status = %s"
        cursor.execute(query + " ORDER BY t.created_at DESC", (status_filter,))
    else:
        cursor.execute(query + " ORDER BY t.created_at DESC")
    
    thoughts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return thoughts

def get_summary_stats():
    """Get summary statistics for the dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get status counts
    cursor.execute("""
        SELECT 
            COUNT(*) as total_thoughts,
            COUNT(*) FILTER (WHERE status = 'APPROVED') as approved,
            COUNT(*) FILTER (WHERE status = 'REJECTED') as rejected,
            COUNT(*) FILTER (WHERE status = 'IN_REVIEW') as in_review,
            COUNT(*) FILTER (WHERE status = 'REMOVED') as removed,
            SUM(thumbs_up) as total_thumbs_up,
            SUM(thumbs_down) as total_thumbs_down
        FROM thoughts
    """)
    
    stats = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return stats

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Get status filter from query parameter
        status_filter = request.args.get('status', 'ALL')
        
        thoughts = get_thoughts_with_stats(status_filter)
        stats = get_summary_stats()
        
        return render_template('dashboard.html', 
                             thoughts=thoughts, 
                             stats=stats,
                             selected_status=status_filter,
                             error=None)
    except Exception as e:
        return render_template('dashboard.html', 
                             thoughts=[], 
                             stats={},
                             selected_status='ALL',
                             error=str(e))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin panel for running custom SQL queries"""
    results = None
    columns = None
    error = None
    query = ""
    row_count = 0
    
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        
        if query:
            try:
                conn = get_db_connection()
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Execute the query
                cursor.execute(query)
                
                # Check if query returns results (SELECT queries)
                if cursor.description:
                    results = cursor.fetchall()
                    row_count = len(results)
                    
                    # Get column names
                    if results:
                        columns = list(results[0].keys())
                    else:
                        columns = [desc[0] for desc in cursor.description]
                else:
                    # For INSERT, UPDATE, DELETE queries
                    conn.commit()
                    row_count = cursor.rowcount
                    results = []
                    columns = []
                
                cursor.close()
                conn.close()
                
            except Exception as e:
                error = str(e)
    
    return render_template('admin.html',
                         query=query,
                         results=results,
                         columns=columns,
                         row_count=row_count,
                         error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

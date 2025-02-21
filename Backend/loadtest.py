import asyncio
import asyncpg
import time

# Database connection settings
DATABASE_URL = "postgresql://Henry:Naseby2411@localhost:5432/BackendDb"

# Number of concurrent connections (simulating multiple users)
NUM_CONNECTIONS = 50000000
NUM_QUERIES = 1000000000

# Sample query for load testing (e.g., INSERT or SELECT)
SQL_QUERY = """
INSERT INTO users (email, password, username, user_status)
VALUES ($1, $2, $3, $4);
"""

# Function to run a single query
async def run_query(connection, user_id, user_specific_id):
    try:
        # Execute the SQL query
        await connection.execute(SQL_QUERY, f"user{user_id}_{user_specific_id}@example.com", f"password{user_id}_{user_specific_id}", f"username{user_id}_{user_specific_id}", "active")
    except Exception as e:
        print(f"Error running query: {e}")

# Function to simulate load
async def simulate_load():
    # Create a connection pool for multiple concurrent connections
    pool = await asyncpg.create_pool(dsn=DATABASE_URL)

    # Start the timer to measure performance
    start_time = time.time()

    # Simulate multiple queries with concurrent connections
    tasks = []
    for i in range(NUM_CONNECTIONS):
        for j in range(NUM_QUERIES // NUM_CONNECTIONS):  # Divide queries across connections
            tasks.append(run_query(pool, i+1, j+1))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

    # End the timer
    end_time = time.time()
    print(f"Completed {NUM_QUERIES} queries in {end_time - start_time:.2f} seconds.")

# Start the load test
if __name__ == "__main__":
    asyncio.run(simulate_load())
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys

# Database connection
DATABASE_URL = 'postgresql://henry:Naseby2411@localhost:5432/BackendDb'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def migrate_database():
    """Add document-whiteboard association table to existing database"""
    
    with engine.connect() as conn:
        try:
            # Check if table already exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'document_whiteboard'
                );
            """))
            
            table_exists = result.scalar()
            
            if table_exists:
                print("document_whiteboard table already exists")
                return True
            
            # Create the association table
            conn.execute(text("""
                CREATE TABLE document_whiteboard (
                    document_id INTEGER NOT NULL,
                    whiteboard_id INTEGER NOT NULL,
                    CONSTRAINT fk_document_whiteboard_document_id 
                        FOREIGN KEY (document_id) REFERENCES notes(id) ON DELETE CASCADE,
                    CONSTRAINT fk_document_whiteboard_whiteboard_id 
                        FOREIGN KEY (whiteboard_id) REFERENCES notes(id) ON DELETE CASCADE,
                    CONSTRAINT uq_document_whiteboard 
                        UNIQUE (document_id, whiteboard_id)
                );
            """))
            
            # Create indexes for better performance
            conn.execute(text("""
                CREATE INDEX idx_document_whiteboard_document_id 
                ON document_whiteboard(document_id);
            """))
            
            conn.execute(text("""
                CREATE INDEX idx_document_whiteboard_whiteboard_id 
                ON document_whiteboard(whiteboard_id);
            """))
            
            conn.commit()
            print("Successfully created document_whiteboard table and indexes")
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"Error during migration: {e}")
            return False

if __name__ == "__main__":
    print("Starting database migration...")
    success = migrate_database()
    if success:
        print("Migration completed successfully!")
        sys.exit(0)
    else:
        print("Migration failed!")
        sys.exit(1)
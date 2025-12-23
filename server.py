import grpc
from concurrent import futures
import sqlite3
import glossary_pb2
import glossary_pb2_grpc

class GlossaryServicer(glossary_pb2_grpc.GlossaryServicer):
    def __init__(self):
        self.conn = sqlite3.connect("glossary.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT UNIQUE,
                description TEXT
            )
        """)
        self.conn.commit()

    def GetTerm(self, request, context):
        self.cursor.execute("SELECT term, description FROM terms WHERE term = ?", (request.term,))
        result = self.cursor.fetchone()
        if result:
            return glossary_pb2.TermReply(term=result[0], description=result[1])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Term not found')
            return glossary_pb2.TermReply()

    def AddTerm(self, request, context):
        try:
            self.cursor.execute(
                "INSERT INTO terms (term, description) VALUES (?, ?)",
                (request.term, request.description)
            )
            self.conn.commit()
            return glossary_pb2.TermReply(term=request.term, description=request.description)
        except sqlite3.IntegrityError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Term already exists')
            return glossary_pb2.TermReply()

    def UpdateTerm(self, request, context):
        self.cursor.execute("UPDATE terms SET description = ? WHERE term = ?",
                            (request.description, request.term))
        self.conn.commit()
        if self.cursor.rowcount == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Term not found')
            return glossary_pb2.TermReply()
        return glossary_pb2.TermReply(term=request.term, description=request.description)

    def DeleteTerm(self, request, context):
        self.cursor.execute("DELETE FROM terms WHERE term = ?", (request.term,))
        self.conn.commit()
        if self.cursor.rowcount == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Term not found')
            return glossary_pb2.TermReply()
        return glossary_pb2.TermReply(term=request.term)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServicer_to_server(GlossaryServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
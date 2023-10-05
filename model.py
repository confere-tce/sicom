from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://snrmyrdk:WdWoPvt6qtVm9uq8V93rSYGKkf3WW-nt@tuffi.db.elephantsql.com/snrmyrdk'

db = SQLAlchemy(app)

class CBPSICOM(db.Model):
    __tablename__ = 'cbpsicom'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String)
    modulo = db.Column(db.String)
    arquivo = db.Column(db.String)
    seq1 = db.Column(db.String)
    seq2 = db.Column(db.String)
    seq3 = db.Column(db.String)
    seq4 = db.Column(db.String)
    seq5 = db.Column(db.String)
    seq6 = db.Column(db.String)
    seq7 = db.Column(db.String)
    seq8 = db.Column(db.String)
    seq9 = db.Column(db.String)
    seq10 = db.Column(db.String)
    seq11 = db.Column(db.String)
    seq12 = db.Column(db.String)
    seq13 = db.Column(db.String)
    seq14 = db.Column(db.String)
    seq15 = db.Column(db.String)
    seq16 = db.Column(db.String)
    seq17 = db.Column(db.String)
    seq18 = db.Column(db.String)
    seq19 = db.Column(db.String)
    seq20 = db.Column(db.String)
    seq21 = db.Column(db.String)
    seq22 = db.Column(db.String)
    seq23 = db.Column(db.String)
    seq24 = db.Column(db.String)
    seq25 = db.Column(db.String)
    seq26 = db.Column(db.String)
    seq27 = db.Column(db.String)
    seq28 = db.Column(db.String)
    seq29 = db.Column(db.String)
    seq30 = db.Column(db.String)

    def __init__(self, usuario, modulo, arquivo, seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9, seq10, seq11, seq12, seq13, seq14, seq15, seq16, seq17, seq18, seq19, seq20, seq21, seq22, seq23, seq24, seq25, seq26, seq27, seq28, seq29, seq30):
        self.usuario = usuario
        self.modulo = modulo
        self.arquivo = arquivo
        self.seq1 = seq1
        self.seq2 = seq2
        self.seq3 = seq3
        self.seq4 = seq4
        self.seq5 = seq5
        self.seq6 = seq6
        self.seq7 = seq7
        self.seq8 = seq8
        self.seq9 = seq9
        self.seq10 = seq10
        self.seq11 = seq11
        self.seq12 = seq12
        self.seq13 = seq13
        self.seq14 = seq14
        self.seq15 = seq15
        self.seq16 = seq16
        self.seq17 = seq17
        self.seq18 = seq18
        self.seq19 = seq19
        self.seq20 = seq20
        self.seq21 = seq21
        self.seq22 = seq22
        self.seq23 = seq23
        self.seq24 = seq24
        self.seq25 = seq25
        self.seq26 = seq26
        self.seq27 = seq27
        self.seq28 = seq28
        self.seq29 = seq29
        self.seq30 = seq30
        

    def salva(usuario, modulo, arquivo, seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9, seq10, seq11, seq12, seq13, seq14, seq15, seq16, seq17, seq18, seq19, seq20, seq21, seq22, seq23, seq24, seq25, seq26, seq27, seq28, seq29, seq30):
        cbpsicom = CBPSICOM(
            usuario,
            modulo,
            arquivo,
            seq1,
            seq2,
            seq3,
            seq4,
            seq5,
            seq6,
            seq7,
            seq8,
            seq9,
            seq10,
            seq11,
            seq12,
            seq13,
            seq14,
            seq15,
            seq16,
            seq17,
            seq18,
            seq19,
            seq20,
            seq21,
            seq22,
            seq23,
            seq24,
            seq25,
            seq26,
            seq27,
            seq28,
            seq29,
            seq30 
            )
        db.session.add(cbpsicom)
        db.session.commit()
        return True

    def create():
        db.create_all()

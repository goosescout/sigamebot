from data import db_session
from data.packs import Pack
from flask_restful import reqparse, abort, Resource
from flask import jsonify
import json

parser = reqparse.RequestParser()
parser.add_argument('game', required=True)
parser.add_argument('user_id', required=True, type=int)


def abort_if_pack_not_found(pack_id):
    session = db_session.create_session()
    pack = session.query(Pack).get(pack_id)
    if not pack:
        abort(404, message=f"Game {pack_id} not found")


class PackResource(Resource):
    def get(self, pack_id):
        abort_if_pack_not_found(pack_id)
        session = db_session.create_session()
        pack = session.query(Pack).get(pack_id)
        with open(pack.game) as f:
            data = json.load(f)
        return data

    def delete(self, pack_id):
        abort_if_pack_not_found(pack_id)
        session = db_session.create_session()
        pack = session.query(Pack).get(pack_id)
        session.delete(pack)
        session.commit()
        return jsonify({'success': 'OK'})

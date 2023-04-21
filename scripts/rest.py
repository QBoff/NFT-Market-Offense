from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from security import encrypt_image
from models import db_session
from models.nfts import NFT


nft_general_parser = reqparse.RequestParser()
nft_general_parser.add_argument("name", required=True, type=str)
nft_general_parser.add_argument("description", required=True, type=str)
nft_general_parser.add_argument("cost", required=True, type=float)
nft_general_parser.add_argument("on_sale", required=True, type=bool)

nft_post_parser = reqparse.RequestParser()
nft_post_parser.add_argument('image', type=bytes,  location=('nft_image',), required=True)


def abort_if_nft_not_found(nft_id):
    session = db_session.create_session()
    news = session.query(NFT).filter(NFT.id == nft_id).first()
    if news is None:
        abort(404, message=f"NFT {nft_id} not found")


class NFTResource(Resource):
    def get(self, nft_id):
        abort_if_nft_not_found(nft_id)
        db = db_session.create_session()
        nft = db.query(NFT).filter(NFT.id == nft_id).first()
        return jsonify(nft.to_dict(only=("name", "description", "cost", "publish_date", "owner")))

    def put(self, nft_id):
        abort_if_nft_not_found(nft_id)
        args = nft_general_parser.parse_args(strict=True)

        db = db_session.create_session()
        nft = db.query(NFT).filter(NFT.id == nft_id).first()

        nft.name = args.name
        nft.description = args.description
        nft.cost = args.cost
        nft.on_sale = args.on_sale

        db.commit()
        return jsonify({"state": "success"})

    def post(self):
        db = db_session.create_session()
        partial_args = nft_general_parser.parse_args()
        args = nft_post_parser.parse_args(req=partial_args)

        newNft = NFT(
            name=args.name,
            cost=args.cost,
            description=args.description,
            image=encrypt_image(args.image),
            on_sale=args.on_sale
        )

class NFTListResource(Resource):
    def get(self, nft_Id):
        pass
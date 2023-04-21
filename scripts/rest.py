from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
from functools import wraps
from scripts.security import encrypt_image
from models import db_session
from models.nfts import NFT
from models.users import User


nft_general_parser = reqparse.RequestParser()
nft_general_parser.add_argument("name", required=True, type=str)
nft_general_parser.add_argument("description", required=True, type=str)
nft_general_parser.add_argument("cost", required=True, type=float)
nft_general_parser.add_argument("on_sale", required=True, type=bool)

nft_post_parser = reqparse.RequestParser()
nft_post_parser.add_argument("image", type=bytes,  location=('nft_image',), required=True)

nft_amount_parser = reqparse.RequestParser()
nft_amount_parser = nft_amount_parser.add_argument("limit", type=int, required=False)


def requires_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-KEY", None)
        if api_key is None:
            return abort(401, message="Missing API key")
        db = db_session.create_session()
        user = db.query(User).filter(User.api_key == api_key).first()
        if user is None:
            return abort(401, message="Invalid API key")
        return func(*args, **kwargs, requesting_user=user)
    return wrapper


def abort_if_nft_not_found(nft_id):
    session = db_session.create_session()
    news = session.query(NFT).filter(NFT.id == nft_id).first()
    if news is None:
        abort(404, message=f"NFT {nft_id} not found")


class NFTResource(Resource):
    @requires_api_key
    def get(self, nft_id, requesting_user):
        print(requesting_user.login)
        abort_if_nft_not_found(nft_id)
        db = db_session.create_session()
        nft = db.query(NFT).filter(NFT.id == nft_id).first()
        return jsonify(nft.to_dict(only=("name", "description", "cost", "publish_date", "owner")))

    @requires_api_key
    def put(self, nft_id, requesting_user):
        abort_if_nft_not_found(nft_id)
        args = nft_general_parser.parse_args(strict=True)

        db = db_session.create_session()
        nft = db.query(NFT).filter(NFT.id == nft_id).first()
        if nft.owner != requesting_user.id:
            return abort(403, "Forbidden")

        nft.name = args.name
        nft.description = args.description
        nft.cost = args.cost
        nft.on_sale = args.on_sale

        db.commit()
        return jsonify({"state": "success"})


class NFTResourcePOST(Resource):
    @requires_api_key
    def post(self, requesting_user):
        db = db_session.create_session()
        partial_args = nft_general_parser.parse_args()
        args = nft_post_parser.parse_args(req=partial_args)

        existingNFT = db.query(NFT).filter(NFT.name == args.name).first()
        if existingNFT is not None:
            return abort(409, message="NFT name is already taken")

        newNft = NFT(
            name=args.name,
            cost=args.cost,
            description=args.description,
            image=encrypt_image(args.image),
            on_sale=args.on_sale,
            owner=requesting_user.id
        )

        db.add(newNft)
        db.commit()
        return jsonify({"state": "success"})


class NFTListResource(Resource):
    @requires_api_key
    def get(self, **kwargs):
        amount = nft_amount_parser.parse_args()
        db = db_session.create_session()
        nfts = db.query(NFT).order_by(NFT.times_sold, NFT.name)
        if amount.limit >= 0:
            nfts = nfts.limit(amount.limit)
        nfts = nfts.all()
        return jsonify([nft.to_dict(only=("name", "description", "cost", "publish_date", "owner")) for nft in nfts])


class UserResource(Resource):
    @requires_api_key
    def get(self, user_id, **kwargs):
        db = db_session.create_session()
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return abort(404, message="User not found")

        userObj = user.to_dict(only=("login", "created_date", "crypto_wallet", "id"))
        userObj["nfts"] = [nft.to_dict(only=("name", "description", "cost", "publish_date", "on_sale")) for nft in user.nfts]

        return jsonify(userObj)

import dbm
from flask import Flask, appcontext_popped, make_response, request, json, jsonify
import models

from flask_mail import Mail, Message
app = Flask(__name__)
app.config.update(dict(
	SECRET_KEY="This is an INSECURE secret!! DO NOT use this in production!!",
	SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root:test@product_db/product",
	SQLALCHEMY_TRACK_MODIFICATIONS=False),
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='dodocazabat@gmail.com',
    MAIL_PASSWORD='qwpm hrfp kway geww',
    MAIL_DEFAULT_SENDER='dodocazabat@gmail.com'
)


mail = Mail(app)
models.init_app(app)
models.create_tables(app)


@app.route('/api/product/create',methods=['POST'])
def post_register():
    
	name = request.form['name']
	seller = request.form['seller']
	price = request.form['price']
	email_Buyer = request.form['email_Buyer']

	item = models.Product()
	item.name = name
	item.seller = seller
	item.price = price
	item.email_Buyer = email_Buyer

	models.db.session.add(item)
	models.db.session.commit()

	response = jsonify({'message':'Product added','product':item.to_json()})

	return response



@app.route('/api/start_delivery/<int:product_id>', methods=['GET'])
def start_delivery(product_id):
    product = models.Product.query.get(product_id)
    product.status = 'In progress'
    models.db.session.commit()

    msg = Message("Product Delivery Instructions",recipients=[product.seller])
    msg.body = "Please prepare to deliver the product : " + product.name   
    try:
        mail.send(msg)
        return jsonify({'message': 'Delivery process started'}), 200
    except Exception as e:
        # Gérer l'exception si nécessaire
        print(e)
        # Envoyer la notification au vendeur
        return jsonify({'message': 'error'}), 500

        
        

    
@app.route('/api/start_pay/<int:product_id>', methods=['GET'])
def start_pay(product_id):
    product = models.Product.query.get(product_id)
    product.buyer = True
    models.db.session.commit()
    msg = Message("Product Paiement Instructions",recipients=[product.email_Buyer])
    msg.body = "Please to pay the product : " + product.name   +" please make a transfert of " +str(product.price)+" $ to account XXXX "
    try:
        mail.send(msg)
        return jsonify({'message': 'Paiement process started'}), 200
    except Exception as e:
        # Gérer l'exception si nécessaire
        print(e)
        # Envoyer la notification au vendeur

        return jsonify({'message': 'Error'}), 500
           
@app.route('/api/reveive_paiement/<int:product_id>', methods=['GET'])
def reveive_paiement(product_id):
    product = models.Product.query.get(product_id)
    product.paiementconfirm = True
    models.db.session.commit()
    msg = Message("Paiement validate",recipients=[product.email_Buyer])
    msg.body = "The seller have been receive the paiement of  : " +str(product.price)+" for the product : "+ product.name 
    try:
        mail.send(msg)
        return jsonify({'message': 'Paiement receive'}), 200
    except Exception as e:
        # Gérer l'exception si nécessaire
        print(e)
        # Envoyer la notification au vendeur

        return jsonify({'message': 'Error'}), 500



@app.route('/api/products',methods=['GET'])
def get_users():
	data = []
	for row in models.Product.query.all():
		data.append(row.to_json())
	response = jsonify({'results':data})
	return response



@app.route('/api/product/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = models.Product.query.get(product_id)
    if product:
        models.db.session.delete(product)
        models.db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
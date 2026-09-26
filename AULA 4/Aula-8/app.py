from flask import Flask
from models.database import init_db
from controllers.classifier_controller import classifier_bp

app = Flask(__name__)
init_db()

app.register_blueprint(classifier_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
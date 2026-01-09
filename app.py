from src import create_app, db


app = create_app()

if __name__ == "__main__":
    print("HerAura is running.........................")

    app.run(host='0.0.0.0', port=5000, debug=True)
    print("Terminating HerAura app.........................")

from website import create_app as cp

app = cp()

if __name__ == "__main__":    app.run(host="0.0.0.0", debug=True)


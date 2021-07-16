from website import create_app

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True)
   app.run(debug=False)

# def mainapp():
#     app = create_app()
#     app.run(debug = False)
#
# if __name__ == '__main__':
#     mainapp()
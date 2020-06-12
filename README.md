# aposto-server

Aposto is a 💸 free, 🌱 light, ✨ easy-to-use and 📖 open-source billing software dedicated to Swiss therapist. It allows generating invoices in compliance with new standard Tarif 590 in a few seconds.

🔥 Aposto is already online on [app.aposto.ch](https://app.aposto.ch/). Find a full introduction to its features on [aposto.ch](https://aposto.ch/).

🇫🇷 Note that Aposto is currently only available in French.

This repository contains the API server the application is using. This server is responsible for 🧾 generating the PDF invoice or 💌 sending the PDF invoice by email to the patient and the therapist using [SendInBlue](https://fr.sendinblue.com/) mailing service.

This API server is designed using [Starlette](https://www.starlette.io/) lightweight framework in Python.

_[Link to the Web application repository](https://github.com/etceterra/aposto-app/)_

## Dependencies

To run the Aposto API on your machine, you need:

* `python3.*` _([download link](https://www.python.org/downloads/) - [after installation](https://packaging.python.org/tutorials/installing-packages/#id12))_
* `pip3.*` _(ensure pip is [installed](https://packaging.python.org/tutorials/installing-packages/#id13) and [up to date](https://packaging.python.org/tutorials/installing-packages/#id14))_

And that's it! The project will install all the Python module dependencies itself on the next step. 🤙

## Quick start

In the terminal of your choice, go through the following steps:

* Install the project: `make install` _→ It creates the Python virtual environment and installs all the needed Python modules._<br>**Note:** You only have to run this command the first time.
* Start the project: `make start` _→ It launches the server on 4 workers._
* **Or** start the project in developer mode: `make dev` _→ It starts the project with a watcher **but only 1 worker**. The server automatically reloads when you edit files._

You're done! The server is now running on http://localhost:8080/. 🚀

## Documentation

Read the [API documentation](https://api.aposto.ch/doc)

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

You're done! The server is now running on http://localhost:8080/. 🚀

## Invoice content structure

The invoice content is a JSON object. Its structure should be as follow:

* **`author`**
    * **`name`**: The author name. It can be a therapist organisation name or the first name and the last name of a therapist.
    * **`street`**: The author box number and street name.
    * **`ZIP`**: The author postal code.
    * **`city`**: The author city.
    * **`phone`**: The author phone number.
    * **`email`**: The author email.
    * **`RCCNumber`**: The author RCC number.
    * **`GLNNumber`**: The author GLN number.
* **`therapist`**
    * **`firstName`**: The therapist first name.
    * **`lastName`**: The therapist first name.
    * **`street`**: The therapist box number and street name.
    * **`ZIP`**: The therapist postal code.
    * **`city`**: The therapist city.
    * **`phone`**: The therapist phone number.
    * **`email`**: The therapist email.
    * **`RCCNumber`**: The therapist RCC number.
    * **`GLNNumber`**: The therapist GLN number.
* **`patient`**
    * **`firstName`**: The patient first name.
    * **`lastName`**: The patient first name.
    * **`street`**: The patient box number and street name.
    * **`ZIP`**: The patient postal code.
    * **`city`**: The patient city.
    * **`canton`**: The patient Swiss canton.
    * **`birthdate`**: The patient birthdate.
    * **`gender`**: The patient gender.
    * **`email`**: The patient email.
* **`servicePrice`**: The hourly price.
* **`services`**: An array of service objects:
    * **`date`**: The date when the service was performed.
    * **`duration`**: The service duration in minutes.
    * **`code`**: The service code as defined by the Tarif 590 standard.
* **`timestamp`**: The JavaScript timestamp identifying the invoice.


## Endpoints

### **GET** `/pdf/{invoice_content_base_64}/{filename}`

🧾 Generate a PDF invoice in the folder `/out/{author.name}/{author.RCCNumber}/{filename}`.

#### Parameters

* `invoice_content_base_64`: The invoice content represented as JSON and encoded in base64. _See [Invoice content structure](#invoice-content-structure)_
* `filename`: The PDF invoice filename. It should end with _.pdf_ extension.

#### Response

* 👌 **Code:** `200`
    <br>**Body:** The PDF file

### **GET** `/email/{invoice_content_base_64}`

💌 Generate and send the PDF invoice to the author and the patient.

#### Parameters

* `invoice_content_base_64`: The invoice content represented as JSON and encoded in base64. _See [Invoice content structure](#invoice-content-structure)_

#### Response

* 👌 **Code:** `200`
    <br>**Body:** Empty
* 👎 **Code:** `400`
    <br>**Body:** A JSON object
    * **`code`**: An error code
    * **`message`**: A readable message associated with the error code

### **POST** `/gln`

🔍 Return the GLN number associated with a therapist or a therapist organisation, fetched from [Refdata](https://www.refdata.ch/fr/partenaires/requete/base-de-donnees-des-partenaires-gln).

#### Request body

A JSON object
* **`name`**: _Optional_. The therapist organisation name. If `name` is provided, `firstName` and `lastName` are ignored.
* **`firstName`**: _Optional_. The therapist first name. If `firstName`is provided, `lastName` is also expected.
* **`lastName`**: _Optional_. The therapist last name. If `lastName`is provided, `firstName` is also expected.
* **`ZIP`**: _Optional_. The therapist postal code.
* **`city`**: _Optional_. The therapist last name.

#### Response

* 👌 **Code:** `200`
    <br>**Body:** HTML text corresponding to the response from https://refdatabase.refdata.ch/Viewer/SearchPartnerJur?Lang=fr or https://refdatabase.refdata.ch/Viewer/SearchPartnerNat?Lang=fr. This HTML contains a form and a table in which the therapist may be present.
* 👎 **Code:** `400`
    <br>**Body:** A JSON object
    * **`name`**: An error message. Neither `name` nor `firstName` and `lastName` parameters are provided in the request body.

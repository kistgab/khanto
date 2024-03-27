# Property rental system for Khanto

This is a basic property rental system for a fictitious company named Khanto. You can check more about the API in the [Features section](#features)

## How to run the project

### By docker

First of all, have Docker installed.
and then just run

```shell
docker compose up
```

now the application is running locally in the adress http://localhost:8000/

# Features

## Properties API

### List all

`GET api_uri/properties/` returns a list of all properties

### Detail one

`GET api_uri/properties/:id/` returns details of the specified id's property

### Create

`POST api_uri/properties/` creates a new property

#### Request body

All of the following fields are required

- max_guests: integer
- bathroom_count: integer
- accept_pets: boolean
- cleaning_fee: decimal
- activation_date: date

### Update all fields

`PUT api_uri/properties/:id` updates the whole existing property

All of the following fields are required

- max_guests: integer
- bathroom_count: integer
- accept_pets: boolean
- cleaning_fee: decimal
- activation_date: date

### Update some fields

`PATCH api_uri/properties/:id` update just some specified fields of an existing property

All of the following fields are optional

- max_guests: integer
- bathroom_count: integer
- accept_pets: boolean
- cleaning_fee: decimal
- activation_date: date

### Delete

`DELETE api_uri/properties/:id` deletes a property

## Advertisement API

### List all

`GET api_uri/advertisements/` returns a list of all advertisements

### Detail one

`GET api_uri/advertisements/:id/` returns details of the specified id's advertisement

### Create

`POST api_uri/advertisements/` creates a new advertisement

#### Request body

All of the following fields are required

- platform_name: string,
- platform_fee: decimal,
- property: integer
  - the id of an existing property

### Update all fields

`PUT api_uri/advertisements/:id` updates the whole existing advertisement

All of the following fields are required

- platform_name: string,
- platform_fee: decimal,
- property: integer
  - the id of an existing property

### Update some fields

`PATCH api_uri/advertisements/:id` update just some specified fields of an existing advertisement

All of the following fields are optional

- platform_name: string,
- platform_fee: decimal,
- property: integer
  - the id of an existing property

## Booking API

### List all

`GET api_uri/bookings/` returns a list of all bookins

### Detail one

`GET api_uri/bookings/:id/` returns details of the specified id's booking

### Create

`POST api_uri/bookings/` creates a new booking

#### Request body

All of the following fields are required

- check_in_date: date,
- check_out_date: date,
- total_value: decimal,
- comments: string (optional),
- total_guests: integer,
- advertisement: integer
  - id of the advertisement that influenced the user to book

### Delete

`DELETE api_uri/bookings/:id` deletes a booking

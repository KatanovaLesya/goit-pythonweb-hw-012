.. GoIT Contacts API (HW12) documentation master file, created by
   sphinx-quickstart on Tue Apr 22 01:00:59 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GoIT Contacts API (HW12) documentation
======================================

This project is a RESTful API for managing personal contacts. It includes features such as authentication, authorization, contact CRUD operations, birthday reminders, and integration with external services like Cloudinary and email.

Use this documentation to explore the available modules, endpoints, and services used in the project.


.. toctree::
   :maxdepth: 2
   :caption: Зміст:

   main
   auth.routes
   auth.service
   auth.dependencies
   routers.contacts
   routers.auth_router
   repository.contacts
   services.email_service
   services.cloudinary_service
   models
   schemas


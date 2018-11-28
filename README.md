# TODO
Write an application for the input of calories

- [x] User must be able to create an account and log in. (If a mobile application, this means that more users can use the app from the same phone).
- [x] When logged in, a user can see a list of his meals, also he should be able to add, edit and delete meals. (user enters calories manually, no auto calculations!)
- [x] Implement at least three roles with different permission levels: a regular user would only be able to CRUD on their owned records, a user manager would be able to CRUD users, and an admin would be able to CRUD all records and users.
- [x] Each entry has a date, time, text, and num of calories.
- [x] Filter by dates from-to, time from-to (e.g. how much calories have I had for lunch each day in the last month if lunch is between 12 and 15h).
- [x] User setting – Expected number of calories per day.
- [ ] When meals are displayed, they go green if the total for that day is less than expected number of calories per day, otherwise they go red.
- [x] REST API. Make it possible to perform all user actions via the API, including authentication (If a mobile application and you don’t know how to create your own backend you can use Firebase.com or similar services to create the API).
- [x] In any case, you should be able to explain how a REST API works and demonstrate that by creating functional tests that use the REST Layer directly. Please be prepared to use REST clients like Postman, cURL, etc. for this purpose.
- [x] If it’s a web application, it must be a single-page application. All actions need to be done client side using AJAX, refreshing the page is not acceptable. (If a mobile application, disregard this).
- [x] Functional UI/UX design is needed. You are not required to create a unique design, however, do follow best practices to make the project as functional as possible.
- [ ] Bonus: unit and e2e tests.

[![Build Status](https://travis-ci.org/johnraysimpson/stream-five-project.svg?branch=master)](https://travis-ci.org/johnraysimpson/stream-five-project)

# Stream Five Project – Tutoring Website

I currently work for a tutoring company which is a small business. I have spoken to the director a number of times about how payments are handled, and how the company can suffer due to complications such as customers paying by cash and not being told that they want to cancel a lesson. This project is aimed towards companies like this, the one I work for has many folders full of information and those were the inspiration of what I wanted to include.

This particular fictional company that this site was made for has several tutoring centres and will possibly be expanding in the future. I see this project as a tool which automates many tasks that prove tedious if done by people, lowering the chances of human error. It is useful for different types of users who have a variety of reasons for using it, hand in hand with a good interface leads me to believe I have created something very unique and powerful.

## UX

This website is aimed towards four types of users, outlined below.

#### Admin users

Although admin users have access to the admin panel on Django, I felt it was important that they have an interface to work with to complete tasks, particularly if I was to sell this to a company that doesn’t have any knowledge of Django. Admin users can:
* Create centres
* Register staff users
* View intake across all of the centres

#### Staff users

Again, although staff users have access to the Django admin panel, they may not necessarily be technology buffs so an interface was required for them to complete the tasks they need to do. These users probably have the most tasks out of all the users, so the list of functionalities is fairly extensive. Staff users can:
* Create, update and delete lessons
* View lessons on a weekly basis
* Register tutor users and assign profile information
* Register parent users and assign profile information
* Add student information to parents
* Build created lessons by populating them with students
* Search for, view and update profile information
* Deactivate, reactivate and delete users
* View the monthly earnings of tutors attached to their centre
* View the payments received from customers (parents) and payments that have been missed

#### Tutor users

Tutor users can:
* View upcoming lessons they are teaching
* View student information for the students coming to their lessons
* View their own profile information
* View their monthly earnings

#### Parent users

Parent users can:
* View upcoming lessons for their child or children
* Pay for lessons and see reminders of past lessons they haven’t paid for
* Cancel future lessons
* View their and their children’s profile information
* View previous payments

I feel that for this type of business it was necessary to give the admin and staff users the majority of control on the website, whereas the role of the tutor and parent users are to view information and pay for services. All users are able to change their password or request a password reset if they can’t remember it.

Wireframes and mockups can be found in the wireframes, mockups and tests folder of this project.

## Features

### Existing Features

Non-user features

* View information in home, about and contact pages
* Login with a login page
* Request a password reset if they already have an account

General Authorised User features

* Change password.
* Logout – returns to the homepage.
* Dashboard – all users have a main dashboard page where they can perform their particular tasks.

Admin User features

* Use a form to add a new centre to the list of centres. This also dynamically updates about and contact pages with relevant information.
* Use a form to add a staff user, with a selector for which centre they work for.
* View payments, which are sorted by month paid. Also returns the previous lessons that have been unpaid across all the centres.

Staff User features

* View the upcoming lessons on a weekly basis, able to view any week, past and present, as long as the input date is a Monday. From here they can add or edit lessons.
* Use a form to add lessons, uses validation to ensure the day and date match, or if the lesson already exists, for example. Same form is used to update a lesson using the lesson as an instance.
* Search, view/edit profile, deactivate, reactivate or delete parent and tutor users. Deactivate and delete functions redirects to a confirmation page in case it was accidently chosen.
* Search, view/edit profile or delete a student. Can also relate students and lessons with an alternative form.
* Add user and profile information for parents and tutors. Once completed an email will be sent from the admin user email with a randomly generated password attached.
* View intake for the centre they work for, also returns previous lessons that haven’t been paid for with contact information of the parent user so they can be contacted about it.

Parent User features

* Use a form to pay for lessons using the Stripe API.
* View and cancel upcoming lessons, also returns any previous lessons pending payment.
* View previous payments made. 
* View profile information for themselves and students they are related to.
* On first time logging in with a randomly generated password, prompted to change it to one they can remember.

Tutor User features

* View upcoming lessons, they can get a glimpse of student information by hovering over a link. Alternatively, the link can be selected to be directed to full profile information of the student.
* View earnings on a monthly basis. 
* View profile information for themselves.
* On first time logging in with a randomly generated password, prompted to change it to one they can remember.

### Features left to implement

* More validation
    * I feel that more validation could have been put in with passwords, such as making sure it has a capital letter etc.
    * At the moment you can add a student to two lessons that run at the same time. More validation could make this less easy to happen.
* Concise python code
    * I fear that the loading times for some requests are too long, for reasons including the amount of records in the database and the code is asking too much. For example, the `get_student_lessons_view` in `lessons/views.py` works, but could probably be made shorter. It appears to timeout when loading in the development running of the site, but seems to be okay on Heroku and I hope it isn’t a problem when being reviewed.
* More styling
    * Although I do have styling and I believe the colour scheme and fonts are well used, I think more styling could have been included to ensure the site looks and feels great. With the sheer amount of pages I had to style unfortunately the time needed for this escape me.
    * The `crispy_forms` library I included seems quite useful in terms of integration with `Bootstrap4`. Grid features can be added, among other things, but with the number of forms I had made time had escaped me.
* More JavaScript uses
    * Although I think the necessary JavaScript components are there, I didn’t feel I got to show off my skills as best as I could, much of the JavaScript was handled by the `Bootstrap4` JavaScript files. I have added my own JavaScript which I feel enhances the use of the site.

## Technologies used

* HTML5
    * all files found in each templates folder
* CSS3
    * for styling purposes, found in static folder
* Bootstrap 4.3.1 CSS and JS libraries
    * for a variety of the layout found in template files.
* Font Awesome 4.7.0
    * for visualisation and information.
* JavaScript and jQuery 3.3.1
    * found in static folder main.js file. Use for hiding and showing of elements. Also hovering links for information.
* Python
    * For backend development, imported libraries include:
        * Django 2.0.7
        * django-crispy-forms 1.8.0 – for form styling
        * Django-tempus-dominus 5.1.2.9 – for date pickers
        * Stripe 2.37.2 – for making payments
        * whitenoise 3.3.1 – for handling static files

## Testing

I would have liked to have used the automatic testing system that Django provides, which I also attempted to do. However, with the amount of code I needed to test I kept getting lost, often thinking “well how do I test this?”. This is something I would like to look further into in the future, for the time being you can find an extensive list of manual tests I performed in the wireframes, mockups and tests folder. This also includes some rationale behind why certain variables were made.

## Deployment

The files in this project have been pushed to my GitHub repository and can be found here https://github.com/johnraysimpson/stream-five-project Each git commit had a meaningful message describing the changes and happened frequently.
The app has been deployed to Heroku using the CLI and can be found here https://zephyr-tuition.herokuapp.com/ 
The environment variables are in heroku so the app can only be seen there, these include:
* a DATABASE_URL
* a SECRET_KEY
* an EMAIL_ADDRESS for gmail
* an EMAIL_PASSWORD for the email account
* STRIPE_PUBLISHABLE
* STRIPE_SECRET
The last two variables would require a Stripe account to be used.

To run the code locally these values would need to be added to an `env.py` file at the top level in this format:

`import os`

`os.environ.setdefault('VARIABLE', 'VALUE')`

## Credits

Links used to help with any areas I found difficult
* Django in 4 hours - https://www.youtube.com/watch?v=F5mRW0jo-U4
* Custom user models - https://www.youtube.com/watch?v=HshbjK1vDtY
* Many answered questions on Stack Overflow
* Adding tooltip changes - http://www.alessioatzeni.com/blog/simple-tooltip-with-jquery-only-text/
The rest of the code was written by myself, although there is a lot of code, I feel my python logic is one of my strongest attributes.

Images
* https://icon-icons.com/icon/weather-wind-windy/108870
* http://iconshow.me/clouds-seamless-background
* https://www.oxfordlearning.com/wp-content/uploads/2018/02/students-working-at-desk.jpeg
* https://indyschild.com/wp-content/uploads/2017/01/tutor-1.jpg
* https://study.com/cimages/course-image/geography-lesson-plans-resources_540889_large.jpeg

Acknowledgements
* Thank you to my current employers for the inspiration of the idea.
* Thank you to the experienced coder Raditha Dissanayake for helping me to get started with this. He offered me just half an hour of help and then there was no stopping me getting this done!

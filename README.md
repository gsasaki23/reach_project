# Reach: A Job-hunt Assistant App
Keep track of all active job applications.\
Built with Django (Python) and Bootstrap


## Future Additions:
* Dashboard
  * Implement "X Days Ago" to replace the updated_at date using [Moment.js](https://momentjs.com/)
  * On an application being moved using Action, blink the moved application [Reference](https://jsfiddle.net/hajtwbot/)
  * On an application being moved using Action, scroll to the section with moved application [Reference](https://www.w3schools.com/jsref/met_element_scrollintoview.asp) 
  * ^^^ above two work, but are commented out due to bootstrap vs jquery bug...
* ADD and EDIT forms
  * Hide the contact section until user selects yes [Reference](https://www.solodev.com/blog/web-design/how-to-hide-form-fields-based-upon-user-selection.stml)
  * Make it pretty in general [Reference](https://www.youtube.com/watch?v=IxRJ8vplzAo)
* Mobile-Friendliness
* Company section pulls Glassdoor API information (ranking, locations, etc)
* Urges user to add 10 new applications a day
* Modal forms and editing info [Reference](https://mdbootstrap.com/docs/jquery/modals/forms/)

## Links
* [Live Site - Under Construction]()
* [Repo](https://github.com/gsasaki23/reach_project.git)
* [Original Wireframe](https://docs.google.com/spreadsheets/d/1ha7PMq2KPLt6nES3qIR5FxazzRbmJ_zZaDzl9nlpyHk/edit#gid=0)
* Deployed automatically using GitHub and [AWS](https://aws.amazon.com/).




## v1.2 (2/28/20):
* UI Changes
  * Minor edits to logo and headers
  * Position and Company details are now popovers

## v1.1 (2/26/20):
* UI Changes
  * Total applications added to header
  * Enabled toggling of each section
* "Contact" Feature added to New, Edit, and Dashboard
* Fixed a bug where some applications were visible to other users

## v1.0 (2/24/20):
* Basic CRUD with Positions, moving positions to different areas given status updates

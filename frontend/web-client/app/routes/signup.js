import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  session: inject(),

  beforeModel(transition) {
    if(this.get('session').isAuthenticated) {
      this.transitionTo('meals.list');
    }
  },

  actions: {
    signup(form) {

      fetch("/api/users", {
        "headers":{
          "content-type":"application/json"
        },
        "body": JSON.stringify({
          user: {
            email: form.get('email'),
            password: form.get('password'),
            name: form.get('name')
          }
        }),
        "method":"POST"
      }).then(response => {
        alert("You have signed up successfully " + form.get('name'));
        this.transitionTo('login');
      }).catch(e => {
        let err = e.errors[0];
        let email = form.get('email');
        alert(`Looks like ${email} is already taken`);
      });
    }
  }
});

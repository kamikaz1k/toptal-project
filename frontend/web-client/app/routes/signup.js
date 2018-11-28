import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  actions: {
    signup(form) {
      console.log(form);

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
        console.log(response);
        alert("You have signed up successfully " + form.get('name'));
        this.transitionTo('login');
      }).catch(e => {
        let err = e.errors[0];
        let email = form.get('email');
        console.log(err);
        alert(`Looks like ${email} is already taken`);
      });
    }
  }
});

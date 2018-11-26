import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  actions: {
    signup(form) {
      console.log(form);

      let user = this.get('store').createRecord('user', {
        email: form.get('email'),
        password: form.get('password'),
        name: form.get('name')
      });

      user.save().then(response => {
        console.log(response);
        alert("You have signed up successfully " + user.get('name'));
        this.transitionTo('login');
      }).catch(e => {
        let err = e.errors[0];
        let email = user.get('email');
        console.log(err);
        alert(`Looks like ${email} is already taken`);
      });
    }
  }
});

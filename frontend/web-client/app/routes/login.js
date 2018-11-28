import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  store: inject(),

  session: inject(),

  actions: {
    login(form) {
      this.get('session').authenticate(
        'authenticator:token-with-revoke',
        {
          email: form.get('email'),
          password: form.get('password')
        }
      ).then(() => {
        this.transitionTo("meals.list");
      }).catch(() => {
        alert("Login failed");
      });
    }
  }
});

import TokenBase from 'ember-simple-auth-token/authenticators/jwt';
import { inject } from '@ember/service';


export default TokenBase.extend({

  session: inject(),

  invalidate() {
    let token = this.get('session.data.authenticated.token');
    return this.makeRequest("/auth/logout", {}, {
      'Authorization': `Bearer ${token}`
    }).finally(() => {
      this._super(...arguments);
    });
  }
});

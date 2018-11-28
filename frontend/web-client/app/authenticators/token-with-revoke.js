import TokenBase from 'ember-simple-auth-token/authenticators/token';

export default TokenBase.extend({
  invalidate(data) {
    let token = data.token;
    return this.makeRequest("/auth/logout", {}, {
      'Authorization': `Bearer ${token}`
    });
  }
});

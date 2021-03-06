import DS from 'ember-data';
import TokenAuthorizerMixin from 'ember-simple-auth-token/mixins/token-authorizer';

export default DS.RESTAdapter.extend(
  TokenAuthorizerMixin, {
  namespace: 'api',
  ensureResponseAuthorized() {/* Ember Simple Auth by default invalidates on 401*/},
});

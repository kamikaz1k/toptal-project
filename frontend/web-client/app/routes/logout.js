import Route from '@ember/routing/route';

export default Route.extend({

  session: Ember.inject.service('session'),

  beforeModel(transition) {
    this.get('session').invalidate().then(() => {
      this.transitionTo('login');
    });
  }

});

import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  session: inject(),

  beforeModel(transition) {
    this.get('session').invalidate().then(() => {
      this.transitionTo('login');
    });
  }

});

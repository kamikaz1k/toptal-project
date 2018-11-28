import Route from '@ember/routing/route';
import { inject } from '@ember/service';

export default Route.extend({

  session: inject(),

  beforeModel(transition) {
    let session = this.get('session');
    session.invalidate().then(() => {
      this.transitionTo('login');
    });
  }

});

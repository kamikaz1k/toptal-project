import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('signup');
  this.route('login');
  this.route('meals', function() {
    this.route('list');
    this.route('new');
    this.route('edit', { path: 'edit/:mealId' });
    this.route('search');
  });
  this.route('logout');

  this.route('users', function() {
    this.route('list');
    this.route('edit', { path: 'edit/:userId' });
    this.route('new');
  });
});

export default Router;

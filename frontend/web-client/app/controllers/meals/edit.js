import Controller from '@ember/controller';
import { computed } from '@ember/object';

export default Controller.extend({

  caloriesForUser: computed('user', function() {
    return this.get('user.caloriesPerDay') || 0;
  }),

  caloriesConsumed: computed('mealsOfDay.@each', function() {
    let calories = 0;
    let mealsOfDay = this.get('mealsOfDay') || [];

    mealsOfDay.forEach(v => {
      calories += v.get('calories');
    });
    return calories;
  }),

  overBudget: computed('caloriesForUser', 'caloriesConsumed', function() {
    let caloriesForUser = this.get('caloriesForUser');
    let caloriesConsumed = this.get('caloriesConsumed');

    if (caloriesForUser && caloriesConsumed) {
      return caloriesConsumed > caloriesForUser;
    }

    return false;
  })

});

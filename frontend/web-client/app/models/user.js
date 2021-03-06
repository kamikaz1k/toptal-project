import DS from 'ember-data';
const { attr } = DS;

export default DS.Model.extend({
  email: attr('string'),
  name: attr('string'),
  caloriesPerDay: attr('number'),
  password: attr('string'),
  active: attr('boolean'),
  isAdmin: attr('boolean', { defaultValue: false }),
  isUserManager: attr('boolean', { defaultValue: false })
});

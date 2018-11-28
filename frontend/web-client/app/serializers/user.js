import { decamelize } from '@ember/string';
import DS from 'ember-data';

export default DS.RESTSerializer.extend({
  keyForAttribute(key, method) {
    return decamelize(key);
  }
});

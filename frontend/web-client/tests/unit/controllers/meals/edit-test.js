import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Controller | meals/edit', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function(assert) {
    let controller = this.owner.lookup('controller:meals/edit');
    assert.ok(controller);
  });
});

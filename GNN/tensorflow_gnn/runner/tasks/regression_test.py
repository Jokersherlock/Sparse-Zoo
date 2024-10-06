# Copyright 2021 The TensorFlow GNN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for node regression."""
from __future__ import annotations
from typing import Sequence, Type

from absl.testing import parameterized
import tensorflow as tf
import tensorflow_gnn as tfgnn

from tensorflow_gnn.runner import interfaces
from tensorflow_gnn.runner.tasks import regression

GraphTensor = tfgnn.GraphTensor
Field = tfgnn.Field

# Enables tests for graph pieces that are members of test classes.
tfgnn.enable_graph_tensor_validation_at_runtime()

READOUT_KEY = "0x8191"
TEST_GRAPH_TENSOR = GraphTensor.from_pieces(
    context=tfgnn.Context.from_fields(
        features={"labels": tf.constant((.8, .1, .9, .1))}
    ),
    node_sets={
        "nodes": tfgnn.NodeSet.from_fields(
            sizes=tf.constant((2, 4, 8, 4)),
            features={
                tfgnn.HIDDEN_STATE: tf.random.uniform((18, 8)),
            },
        )
    },
)


def label_fn(inputs: GraphTensor) -> tuple[GraphTensor, Field]:
  y = inputs.context["labels"]
  x = inputs.remove_features(context=("labels",))
  return x, y


def l2(rate):
  return tf.keras.regularizers.L2(rate)


def add_readout_from_first_node(gt: GraphTensor) -> GraphTensor:
  return tfgnn.add_readout_from_first_node(
      gt,
      key=READOUT_KEY,
      node_set_name="nodes")


def context_readout_into_feature(gt: GraphTensor) -> GraphTensor:
  return tfgnn.experimental.context_readout_into_feature(
      gt,
      feature_name="labels",
      remove_input_feature=True)


class Regression(tf.test.TestCase, parameterized.TestCase):

  def setUp(self):
    super().setUp()
    tfgnn.enable_graph_tensor_validation_at_runtime()

  @parameterized.named_parameters([
      dict(
          testcase_name="GraphMeanAbsoluteErrorLabelFn",
          task=regression.GraphMeanAbsoluteError(
              "nodes",
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanAbsoluteErrorReadout",
          task=regression.GraphMeanAbsoluteError(
              "nodes",
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanAbsolutePercentageErrorLabelFn",
          task=regression.GraphMeanAbsolutePercentageError(
              "nodes",
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanAbsolutePercentageErrorReadout",
          task=regression.GraphMeanAbsolutePercentageError(
              "nodes",
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanSquaredErrorLabelFn",
          task=regression.GraphMeanSquaredError(
              "nodes",
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanSquaredErrorReadout",
          task=regression.GraphMeanSquaredError(
              "nodes",
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanSquaredLogarithmicErrorLabelFn",
          task=regression.GraphMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanSquaredLogarithmicErrorReadout",
          task=regression.GraphMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanSquaredLogScaledErrorLabelFn",
          task=regression.GraphMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="GraphMeanSquaredLogScaledErrorReadout",
          task=regression.GraphMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanAbsoluteErrorLabelFn",
          task=regression.RootNodeMeanAbsoluteError(
              "nodes",
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanAbsoluteErrorReadout",
          task=regression.RootNodeMeanAbsoluteError(
              "nodes",
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanAbsolutePercentageErrorLabelFn",
          task=regression.RootNodeMeanAbsolutePercentageError(
              "nodes",
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanAbsolutePercentageErrorReadout",
          task=regression.RootNodeMeanAbsolutePercentageError(
              "nodes",
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanSquaredErrorLabelFn",
          task=regression.RootNodeMeanSquaredError(
              "nodes",
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanSquaredErrorReadout",
          task=regression.RootNodeMeanSquaredError(
              "nodes",
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanSquaredLogarithmicErrorLabelFn",
          task=regression.RootNodeMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanSquaredLogarithmicErrorReadout",
          task=regression.RootNodeMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanSquaredLogScaledErrorLabelFn",
          task=regression.RootNodeMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_fn=label_fn),
          inputs=TEST_GRAPH_TENSOR,
          expected_gt=TEST_GRAPH_TENSOR.remove_features(context=("labels",)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="RootNodeMeanSquaredLogScaledErrorReadout",
          task=regression.RootNodeMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_feature_name="labels"),
          inputs=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanAbsoluteErrorLabelFn",
          task=regression.NodeMeanAbsoluteError(
              READOUT_KEY,
              label_fn=label_fn),
          inputs=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_gt=add_readout_from_first_node(
              TEST_GRAPH_TENSOR.remove_features(context=("labels",))),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanAbsoluteErrorReadout",
          task=regression.NodeMeanAbsoluteError(
              READOUT_KEY,
              label_feature_name="labels"),
          inputs=add_readout_from_first_node(context_readout_into_feature(
              TEST_GRAPH_TENSOR)),
          expected_gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanAbsolutePercentageErrorLabelFn",
          task=regression.NodeMeanAbsolutePercentageError(
              READOUT_KEY,
              label_fn=label_fn),
          inputs=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_gt=add_readout_from_first_node(
              TEST_GRAPH_TENSOR.remove_features(context=("labels",))),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanAbsolutePercentageErrorReadout",
          task=regression.NodeMeanAbsolutePercentageError(
              READOUT_KEY,
              label_feature_name="labels"),
          inputs=add_readout_from_first_node(context_readout_into_feature(
              TEST_GRAPH_TENSOR)),
          expected_gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanSquaredErrorLabelFn",
          task=regression.NodeMeanSquaredError(
              READOUT_KEY,
              label_fn=label_fn),
          inputs=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_gt=add_readout_from_first_node(
              TEST_GRAPH_TENSOR.remove_features(context=("labels",))),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanSquaredErrorReadout",
          task=regression.NodeMeanSquaredError(
              READOUT_KEY,
              label_feature_name="labels"),
          inputs=add_readout_from_first_node(context_readout_into_feature(
              TEST_GRAPH_TENSOR)),
          expected_gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanSquaredLogarithmicErrorLabelFn",
          task=regression.NodeMeanSquaredLogarithmicError(
              READOUT_KEY,
              units=3,
              label_fn=label_fn),
          inputs=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_gt=add_readout_from_first_node(
              TEST_GRAPH_TENSOR.remove_features(context=("labels",))),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanSquaredLogarithmicErrorReadout",
          task=regression.NodeMeanSquaredLogarithmicError(
              READOUT_KEY,
              units=3,
              label_feature_name="labels"),
          inputs=add_readout_from_first_node(context_readout_into_feature(
              TEST_GRAPH_TENSOR)),
          expected_gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanSquaredLogScaledErrorLabelFn",
          task=regression.NodeMeanSquaredLogScaledError(
              READOUT_KEY,
              units=2,
              label_fn=label_fn),
          inputs=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_gt=add_readout_from_first_node(
              TEST_GRAPH_TENSOR.remove_features(context=("labels",))),
          expected_labels=tf.constant((.8, .1, .9, .1))),
      dict(
          testcase_name="NodeMeanSquaredLogScaledErrorReadout",
          task=regression.NodeMeanSquaredLogScaledError(
              READOUT_KEY,
              units=2,
              label_feature_name="labels"),
          inputs=add_readout_from_first_node(context_readout_into_feature(
              TEST_GRAPH_TENSOR)),
          expected_gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_labels=tf.constant((.8, .1, .9, .1))),
  ])
  def test_preprocess(
      self,
      task: interfaces.Task,
      inputs: GraphTensor,
      expected_gt: Sequence[int],
      expected_labels: Sequence[int]):
    xs, ys = task.preprocess(inputs)

    self.assertEqual(xs.spec, expected_gt.spec)  # Assert `GraphTensor` specs.
    self.assertAllEqual(ys, expected_labels)

  @parameterized.named_parameters([
      dict(
          testcase_name="GraphMeanAbsoluteError",
          task=regression.GraphMeanAbsoluteError(
              "nodes",
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=TEST_GRAPH_TENSOR,
          expected_loss=tf.keras.losses.MeanAbsoluteError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="GraphMeanAbsolutePercentageError",
          task=regression.GraphMeanAbsolutePercentageError(
              "nodes",
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_loss=tf.keras.losses.MeanAbsolutePercentageError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="GraphMeanSquaredError",
          task=regression.GraphMeanSquaredError(
              "nodes",
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=TEST_GRAPH_TENSOR,
          expected_loss=tf.keras.losses.MeanSquaredError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="GraphMeanSquaredLogarithmicError",
          task=regression.GraphMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_loss=tf.keras.losses.MeanSquaredLogarithmicError,
          expected_shape=tf.TensorShape((None, 3)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="GraphMeanSquaredLogScaledError",
          task=regression.GraphMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=TEST_GRAPH_TENSOR,
          expected_loss=regression.MeanSquaredLogScaledError,
          expected_shape=tf.TensorShape((None, 2)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="RootNodeMeanAbsoluteError",
          task=regression.RootNodeMeanAbsoluteError(
              "nodes",
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_loss=tf.keras.losses.MeanAbsoluteError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="RootNodeMeanAbsolutePercentageError",
          task=regression.RootNodeMeanAbsolutePercentageError(
              "nodes",
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=TEST_GRAPH_TENSOR,
          expected_loss=tf.keras.losses.MeanAbsolutePercentageError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="RootNodeMeanSquaredError",
          task=regression.RootNodeMeanSquaredError(
              "nodes",
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_loss=tf.keras.losses.MeanSquaredError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="RootNodeMeanSquaredLogarithmicError",
          task=regression.RootNodeMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=TEST_GRAPH_TENSOR,
          expected_loss=tf.keras.losses.MeanSquaredLogarithmicError,
          expected_shape=tf.TensorShape((None, 3)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="RootNodeMeanSquaredLogScaledError",
          task=regression.RootNodeMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR),
          expected_loss=regression.MeanSquaredLogScaledError,
          expected_shape=tf.TensorShape((None, 2)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="NodeMeanAbsoluteError",
          task=regression.NodeMeanAbsoluteError(
              READOUT_KEY,
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_loss=tf.keras.losses.MeanAbsoluteError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="NodeMeanAbsolutePercentageError",
          task=regression.NodeMeanAbsolutePercentageError(
              READOUT_KEY,
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_loss=tf.keras.losses.MeanAbsolutePercentageError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="NodeMeanSquaredError",
          task=regression.NodeMeanSquaredError(
              READOUT_KEY,
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_loss=tf.keras.losses.MeanSquaredError,
          expected_shape=tf.TensorShape((None, 1)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="NodeMeanSquaredLogarithmicError",
          task=regression.NodeMeanSquaredLogarithmicError(
              READOUT_KEY,
              units=3,
              label_fn=label_fn,
              kernel_regularizer=l2(0.125)),
          gt=add_readout_from_first_node(TEST_GRAPH_TENSOR),
          expected_loss=tf.keras.losses.MeanSquaredLogarithmicError,
          expected_shape=tf.TensorShape((None, 3)),
          expected_l2_regularization=0.125),
      dict(
          testcase_name="NodeMeanSquaredLogScaledError",
          task=regression.NodeMeanSquaredLogScaledError(
              READOUT_KEY,
              units=2,
              label_feature_name="labels",
              kernel_regularizer=l2(0.125)),
          gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR)),
          expected_loss=regression.MeanSquaredLogScaledError,
          expected_shape=tf.TensorShape((None, 2)),
          expected_l2_regularization=0.125),
  ])
  def test_predict(
      self,
      task: interfaces.Task,
      gt: GraphTensor,
      expected_loss: Type[tf.keras.losses.Loss],
      expected_shape: tf.TensorShape,
      expected_l2_regularization: float):
    # Assert head readout, activation and shape.
    inputs = tf.keras.layers.Input(type_spec=gt.spec)
    model = tf.keras.Model(inputs, task.predict(inputs))
    self.assertLen(model.layers, 3)
    self.assertIsInstance(model.layers[0], tf.keras.layers.InputLayer)
    self.assertIsInstance(
        model.layers[1],
        (
            tfgnn.keras.layers.ReadoutFirstNode,
            tfgnn.keras.layers.Pool,
            tfgnn.keras.layers.StructuredReadout,
        ),
    )
    self.assertIsInstance(model.layers[2], tf.keras.layers.Dense)

    _, _, dense = model.layers
    self.assertTrue(expected_shape.is_compatible_with(dense.output_shape))
    self.assertEqual(dense.kernel_regularizer.get_config()["l2"],
                     expected_l2_regularization)

    # Assert losses.
    loss = task.losses()
    self.assertIsInstance(loss, expected_loss)

  @parameterized.named_parameters([
      dict(
          testcase_name="GraphMeanAbsoluteError",
          task=regression.GraphMeanAbsoluteError(
              "nodes",
              label_fn=label_fn),
          gt=TEST_GRAPH_TENSOR),
      dict(
          testcase_name="GraphMeanAbsolutePercentageError",
          task=regression.GraphMeanAbsolutePercentageError(
              "nodes",
              label_feature_name="labels"),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="GraphMeanSquaredError",
          task=regression.GraphMeanSquaredError(
              "nodes",
              label_fn=label_fn),
          gt=TEST_GRAPH_TENSOR),
      dict(
          testcase_name="GraphMeanSquaredLogarithmicError",
          task=regression.GraphMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_feature_name="labels"),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="GraphMeanSquaredLogScaledError",
          task=regression.GraphMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_fn=label_fn),
          gt=TEST_GRAPH_TENSOR),
      dict(
          testcase_name="RootNodeMeanAbsoluteError",
          task=regression.RootNodeMeanAbsoluteError(
              "nodes",
              label_feature_name="labels"),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="RootNodeMeanAbsolutePercentageError",
          task=regression.RootNodeMeanAbsolutePercentageError(
              "nodes",
              label_fn=label_fn),
          gt=TEST_GRAPH_TENSOR),
      dict(
          testcase_name="RootNodeMeanSquaredError",
          task=regression.RootNodeMeanSquaredError(
              "nodes",
              label_feature_name="labels"),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="RootNodeMeanSquaredLogarithmicError",
          task=regression.RootNodeMeanSquaredLogarithmicError(
              "nodes",
              units=3,
              label_fn=label_fn),
          gt=TEST_GRAPH_TENSOR),
      dict(
          testcase_name="RootNodeMeanSquaredLogScaledError",
          task=regression.RootNodeMeanSquaredLogScaledError(
              "nodes",
              units=2,
              label_feature_name="labels"),
          gt=context_readout_into_feature(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="NodeMeanAbsoluteError",
          task=regression.NodeMeanAbsoluteError(
              READOUT_KEY,
              label_feature_name="labels"),
          gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR))),
      dict(
          testcase_name="NodeMeanAbsolutePercentageError",
          task=regression.NodeMeanAbsolutePercentageError(
              READOUT_KEY,
              label_fn=label_fn),
          gt=add_readout_from_first_node(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="NodeMeanSquaredError",
          task=regression.NodeMeanSquaredError(
              READOUT_KEY,
              label_feature_name="labels"),
          gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR))),
      dict(
          testcase_name="NodeMeanSquaredLogarithmicError",
          task=regression.NodeMeanSquaredLogarithmicError(
              READOUT_KEY,
              units=3,
              label_fn=label_fn),
          gt=add_readout_from_first_node(TEST_GRAPH_TENSOR)),
      dict(
          testcase_name="NodeMeanSquaredLogScaledError",
          task=regression.NodeMeanSquaredLogScaledError(
              READOUT_KEY,
              units=2,
              label_feature_name="labels"),
          gt=add_readout_from_first_node(
              context_readout_into_feature(TEST_GRAPH_TENSOR))),
  ])
  def test_fit(
      self,
      task: interfaces.Task,
      gt: GraphTensor):
    inputs = tf.keras.layers.Input(type_spec=gt.spec)
    outputs = task.predict(inputs)
    model = tf.keras.Model(inputs, outputs)

    ds = tf.data.Dataset.from_tensors(gt).repeat().batch(2).take(1)
    ds = ds.map(GraphTensor.merge_batch_to_components).map(task.preprocess)

    model.compile(loss=task.losses(), metrics=task.metrics())
    model.fit(ds)

if __name__ == "__main__":
  tf.test.main()

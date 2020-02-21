# regression
python main.py -config configs/regression/relu_relu_big/base_config.yaml--ac additional_configs/  --en regression_relu_relu_big
python main.py -config configs/regression/relu_relu_small/base_config.yaml--ac additional_configs/ --en regression_relu_relu_small
python main.py -config configs/regression/relu_sigmoid_big/base_config.yaml--ac additional_configs/ --en regression_relu_sigmoid_big
python main.py -config configs/regression/relu_sigmoid_small/base_config.yaml--ac additional_configs/ --en regression_relu_sigmoid_small
python main.py -config configs/regression/sigmoid_relu_big/base_config.yaml--ac additional_configs/ --en regression_sigmoid_relu_big
python main.py -config configs/regression/sigmoid_relu_small/base_config.yaml--ac additional_configs/ --en regression_sigmoid_relu_small
python main.py -config configs/regression/sigmoid_sigmoid_big/base_config.yaml--ac additional_configs/ --en regression_sigmoid_sigmoid_big
python main.py -config configs/regression/sigmoid_sigmoid_small/base_config.yaml--ac additional_configs/ --en regression_sigmoid_sigmoid_small

# classification
python main.py -config configs/classification/relu_relu_big/base_config.yaml --ac additional_configs/ --en clssification_relu_relu_big
python main.py -config configs/classification/relu_relu_small/base_config.yaml --ac additional_configs/ --en clssification_relu_relu_small
python main.py -config configs/classification/relu_sigmoid_big/base_config.yaml --ac additional_configs/ --en clssification_relu_sigmoid_big
python main.py -config configs/classification/relu_sigmoid_small/base_config.yaml --ac additional_configs/ --en clssification_relu_sigmoid_small
python main.py -config configs/classification/sigmoid_relu_big/base_config.yaml --ac additional_configs/ --en clssification_sigmoid_relu_big
python main.py -config configs/classification/sigmoid_relu_small/base_config.yaml --ac additional_configs/ --en clssification_sigmoid_relu_small
python main.py -config configs/classification/sigmoid_sigmoid_big/base_config.yaml --ac additional_configs/ --en clssification_sigmoid_sigmoid_big
python main.py -config configs/classification/sigmoid_sigmoid_small/base_config.yaml --ac additional_configs/ --en clssification_sigmoid_sigmoid_small

# mnist-regression
python main.py -config configs/mnist_regression/relu_relu_big/base_config.yaml --ac additional_configs/ --en mnist_regression_relu_relu_big
python main.py -config configs/mnist_regression/relu_relu_small/base_config.yaml --ac additional_configs/ --en mnist_regression_relu_relu_small
python main.py -config configs/mnist_regression/relu_sigmoid_big/base_config.yaml --ac additional_configs/ --en mnist_regression_relu_sigmoid_big
python main.py -config configs/mnist_regression/relu_sigmoid_small/base_config.yaml --ac additional_configs/ --en mnist_regression_relu_sigmoid_small
python main.py -config configs/mnist_regression/sigmoid_relu_big/base_config.yaml --ac additional_configs/ --en mnist_regression_sigmoid_relu_big
python main.py -config configs/mnist_regression/sigmoid_relu_small/base_config.yaml --ac additional_configs/ --en mnist_regression_sigmoid_relu_small
python main.py -config configs/mnist_regression/sigmoid_sigmoid_big/base_config.yaml --ac additional_configs/ --en mnist_regression_sigmoid_sigmoid_big
python main.py -config configs/mnist_regression/sigmoid_sigmoid_small/base_config.yaml --ac additional_configs/ --en mnist_regression_sigmoid_sigmoid_small

# mnist-classification
python main.py -config configs/mnist_classification/relu_relu_big/base_config.yaml --ac additional_configs/ --en mnist_classification_relu_relu_big
python main.py -config configs/mnist_classification/relu_relu_small/base_config.yaml --ac additional_configs/ --en mnist_classification_relu_relu_small
python main.py -config configs/mnist_classification/relu_sigmoid_big/base_config.yaml --ac additional_configs/ --en mnist_classification_relu_sigmoid_big
python main.py -config configs/mnist_classification/relu_sigmoid_small/base_config.yaml --ac additional_configs/ --en mnist_classification_relu_sigmoid_small
python main.py -config configs/mnist_classification/sigmoid_relu_big/base_config.yaml --ac additional_configs/ --en mnist_classification_sigmoid_relu_big
python main.py -config configs/mnist_classification/sigmoid_relu_small/base_config.yaml --ac additional_configs/ --en mnist_classification_sigmoid_relu_small
python main.py -config configs/mnist_classification/sigmoid_sigmoid_big/base_config.yaml --ac additional_configs/ --en mnist_classification_sigmoid_sigmoid_big
python main.py -config configs/mnist_classification/sigmoid_sigmoid_small/base_config.yaml --ac additional_configs/ --en mnist_classification_sigmoid_sigmoid_small

# pure-mnist
python main.py -config configs/pure_mnist/relu/base_config.yaml --ac additional_configs/ --en pure_mnist_classification_relu
python main.py -config configs/pure_mnist/sigmoid/base_config.yaml --ac additional_configs/ --en pure_mnist_classification_sigmoid
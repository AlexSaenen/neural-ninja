# neural-net-builder

##What is the purpose

Maestro neural net builder is a infrastructure capable of deploying and running several neural network instances
The goal of these networks is to digest data and learn which decisions are the most adapted depending on the input

The infra will be accessible through an API that allows the outside tools and software to progressively feed the networks with new input and get the results


##How to launch

You need to have docker installed to make this work

```
make build
make run
docker logs -f neural-net-builder
```

If you wish to also be able to check TensorBoard for the summary logs created by TensorFlow:

```
make tensorboard
```

And in your browser, go to 'localhost:6006'


##What can the API do ?

The Skynet API is capable of handling a few public and private, static and dynamic paths. Some, it handles directly by replying the data, other requests are sent to the Engine to be processed

Among the public static paths we have the following:
- `/` this is the home path of Skynet and will just return a HTML landing page, with a button to go to the status page (see the following request)
- `/status` shows Skynet's status, meaning it returns a HTML page containing the description, status (running, loaded), configuration rules and accuracy of every Neural Network in the Engine's repository
- `/assets/fileName.ext` this route should only be used by the browser when requesting the assets necessary to load the HTML pages (css, images, fonts ...)

For the following requests, the user or service needs to send in the request body or form an attribute `skynetApiKey` that contains the apiKey used to gain access to private parts of the API. If the sent key doesn't match the expected key, the request will be refused

`/networks/<action>` is destined to handle all networks as a whole, `<action>` here corresponds to an action that will be executed concerning all the requests. For now, the possible actions are `getAll` and `upload`:
- `/networks/getAll` will return all the networks the Engine has in it's repository
- `/networks/upload` allows an user to upload a new network that will be added to the repository (Form request)
Additional request params needed:
    - `networkFile` with as Value an equivalent of fs.StreamReader (NodeJS) on the file that will be uploaded

`/network/<netName>/<action>` will handle all the actions on a network named `<netName>`, `<action>` corresponds to the action that will be executed, possible actions right now are `train`, `predict`, `accuracy`, `load`,
`unload`, `start`, `stop`, `details`:
- `/network/awesomeNetwork/train` will train the network awesomeNetwork
Additional request params needed:
    - `meals` with as Value an array of meals with the structure: `<netName>TrainingInput` where `<netName>` is the name of the net, it will contain all the input, `label` will contain the correct output for this input
- `/network/awesomeNetwork/predict` will make a prediction using the network awesomeNetwork
Additional request params needed:
    - `meals` with as Value an array of meals with the structure: `<netName>TrainingInput` where `<netName>` is the name of the net, it will contain all the input
- `/network/awesomeNetwork/accuracy` will determine the network awesomeNetwork's accuracy
Additional request params needed:
    - `meals` with as Value an array of meals with the structure: `<netName>TrainingInput` where `<netName>` is the name of the net, it will contain all the input, `label` will contain the correct output for this input
- `/network/awesomeNetwork/load` will load the network awesomeNetwork module
- `/network/awesomeNetwork/unload` will unload the network awesomeNetwork module
- `/network/awesomeNetwork/start` will instantiate and start the network awesomeNetwork
- `/network/awesomeNetwork/stop` will stop the network awesomeNetwork
- `/network/awesomeNetwork/delete` will delete awesomeNetwork from the engine's repository
- `/network/awesomeNetwork/usable` tells if the network has been trained enough to be used (if it's accuracy is beyond the usageThreshold)
- `/network/awesomeNetwork/details` will return all the details about a network, it's status (running, loaded), configuration rules and accuracy

`/network/<action>` is destined for the NetKit, the tool that for now creates the networks, `<action>` here corresponds to the action we want the NetKit to handle. For now the only action it can handle is create
So the route `/network/create` is available to whom wishes to create a new network and integrate it to the Engine's repository
Additional request params needed:
    - `netName` with as Value the name of the network that will be created
    - `input` with as Value an array with the name of all the features the network will be based upon
    - `output` with as Value `regression` or `classification`, it describes the networkType and the desired output

##How to manually create and use a Network

Now we'll see how to create manually a network file (NeuNet) that will be managed by the Engine and how we can
interact with it through the API

This tutorial is structured into 2 points:
- creation of a NeuNet and configuration
- upload of the NeuNet


###Creation of a NeuNet


A NeuNet is a python file that contains configuration for the network, functions to instantiate and stop the network, as well as a Python Class inheriting the NeuNetOperator (who inherits NeuNet) Class that describes what the network is and how it will be trained etc...

Let's create a network called studentHours that can have as input the number of hours a student studied and as output it says the probability the student passes the exam

Create a file studentHours.py and follow the tutorial below
We'll start with the configuration

#### The current configuration rules understood by the Engine are the following:

- `autoRun` tells the Engine to automatically instantiate the NeuNet once it detects the presence of the network in its repository, instead of just adding its reference to the repository. The possible values are `True` and `False`. By default it's `True`
- `usageThreshold` corresponds to an accuracy level between 0 and 1, it tells the Engine, when the training brings the network above this accuracy it can be used to make predictions. By default it's `0.8` (80%)
- `inputSelector` tells the underlying network components where to look for the input data in the JSON object received by the request

You can add your own configuration to be used personally further in your network code

Now we'll add our configuration to our file, first of all we need to import the NeuNet file from which we'll grab the default config layout and we'll import a module that allows us to make a shallow copy of the default config object:

```python
import engine.neural.neuNet as baseNet
import copy
```

Great ! Now we don't want the network to autoRun (only for tutorial purposes) and we want a small batchSize of about 15 elements, the usageThreshold should be really accurate so we'll set it at 0.93:

```python
config = copy.copy(baseNet.config)
config['autoRun'] = False
config['batchSize'] = 15
config['usageThreshold'] = 0.93
config['inputSelector'] = 'studentHoursTrainingInput'

COLUMNS = [ 'hours' ]
```

`inputSelector` tells the abstract parts of the NeuNet framework where to look in a meal to get the input data
`COLUMNS` is where we define, in the correct order, which features are present in a meal element

#### The NeuNetOperator and NeuNetRegressor Class

Now we will import the neuNetRegressor module, containing the abstract class from which we'll inherit our own network class, since we want a model that performs regression

Let's start by importing what we need:

```python
from engine.neural.neuNetRegressor import NeuNetRegressor
from engine.neural.operator import Operator
import tensorflow as tf
```

Here we import the NeuNetRegressor class as well as Operator needed by the Engine, and tensorflow for the network

Let's define our class and write the constructor:

```python
class StudentHours(NeuNetRegressor):

    def __init__(self, atomicLock):
        self._config = config
        self._columns = COLUMNS
        super().__init__(atomicLock)
```

The atomicLock variable is a Mutex used by the NeuNetWatcher, a class from the engine that is instantiated for each network and supervises it's operations. The lock is used by both to make atomic operations and make sure this part of the Engine is thread safe (yes we need threads to make everything run smoothly)

The Operator and NeuNetRegressor have a few useful functions we need to override with our own implementation while inheriting the class, while writing these functions, to not forget to leave a one tab indentation

This function is where it gets interesting, `_declareNetwork()` is where we tell the Engine which tensorflow variables we need to make our network run, but we'll also declare how our graph will look like, basically this function is where we define our tensorflow network

**While adding the next functions to your file after the StudentHours' constructor, it's important to leave a 1 tab indentation so the functions are considered part of the StudentHours Class**

```python
def _declareNetwork(self):
    hours = tf.contrib.layers.real_valued_column('hours')

    self.network = tf.contrib.learn.LinearRegressor(
        model_dir=self._backupDir,
        feature_columns=[hours],
        optimizer=tf.train.RMSPropOptimizer(learning_rate=0.01)
    )
```

The network is now created, next we'll see how we can upload and use it

###Upload of the network

Once you launched Skynet we can thanks to curl (install it if you haven't got it) upload our network to the Engine's repository

It is a POST request since we have to send both a file and also a apiKey which will allow the API to approve our request.

This is thus the curl request to upload our studentHours.py file:

```
curl -F "networkFile=@models/studentHours.py" -F "skynetApiKey=skynetSuperSecretApiKey" dev.l0cal/networks/upload
```

Now we need to load the network since we set in the config that `autoRun` should be deactivated:

```
curl -F "skynetApiKey=skynetSuperSecretApiKey" dev.l0cal/network/studentHours/load
```

and also start it:

```
curl -F "skynetApiKey=skynetSuperSecretApiKey" dev.l0cal/network/studentHours/start
```

We have successfully uploaded and loaded our network to the Engine !

##How to create a network through the CreationKit

In this part we want to create a network using Skynet's CreationKit, to do that we just need to send a simple curl to the API with a minimum of configuration

If we stay in the same theme as the previous part, we want to recreate the studentHours network, we can do that with the following curl:

```
curl --data '{ "skynetApiKey": "skynetSuperSecretApiKey", "netName": "studentHours", "input": ["hours"], "output": "regression" }' -H "Content-type: application/json" dev.l0cal/network/create
```

The params are the following:
- `netName` name of the network you want to create
- `input` an array of strings, each string represents the name of a feature you will pass in the input data. Although you won't send the name but only it's assigned data through the API, we need it when creating the network to explain the order in which the features will be sent and create the columns that will host the data. Therefore it is extremely important to send the feature names in the same order you will send the feature values in the next batches.
- `output` defines the output scheme and thus the network type, can accept `regression` (convergence of all the input to an output value between 0 and 1) and `classification` (output of an integer representing the predicted category)
- `templateBindings` is a dictionary that contains as keys the names of bindings available in the template (for now you can find the different keys in src/netKit/templates/basic.py), the values of those keys will thus override the default bindings generated by the creationKit

If we want to create a Deep Network such as autoBuy, use the following curl:

```
curl --data '{ "skynetApiKey": "skynetSuperSecretApiKey", "netName": "autoBuy", "input": ["days_sold_out","margin_ratio","places_left","sold_out_in","stock_duration","tickets_bought","tickets_sold","turnover"], "output": "classification" }' -H "Content-type: application/json" dev.l0cal/network/create
```

In the next part we'll see how to interact with the network studentHours we created in the manual and automatic parts of this tutorial

##Interaction with the network

For the next curls, they are too long (we pass the data as body) so you can find them in `unitTests/curlTestsStudentHours.sh`

First we'll tell the network to train (it's the third curl from the file), the data consists of a few hundred elements containing hours studied and the correct probability the student will pass the exam

Next, we will ask the network to predict the probabilities of each hour (5th curl from the file)

And finally we'll ask the accuracy of the network (6th curl), it should read 0.94 (94%) or something in that range

The full code of `studentHours.py` can be found in `unitTests/studentHours.py`

# Fictionary
Create fictionary datasets and documents from templates, jsons or text. 

---
## How to get started

Let start with an easy example by manually choosing our fictive elements.

```
from fictionary import Fictionary

fn = Fictionary()

my_first_name = fn.choose("firstname")
my_city = fn.choose("city")

print(f"Hi, my name is {my_first_name} and I am from {my_city}.")
```

This is how our first result could look like: 
``Hi, my name is Anna and I am from New York.``


You can also get more specific fictions by passing a origin:
```
my_first_name = fn.choose("firstname", "slavik")
my_city = fn.choose("city", "germany")
```
Now the result will more like this:
``Hi, my name is Swetlana and I am from Wolfratshausen.``




---
## FictionaryJson
Use a json structure which will be filled with fictionary data. 

##### Syntax
```
from fictionary import Fictionary, FictionaryJson

fn = Fictionary()

my_element = FictionaryJson()

my_element.json = {
                    "my_first_name":"firstname:slavik",
                    "location":"city:germany"
                  }

output = fn.generate(my_element)  # Can be used in reverse aswell: my_element.generate(fn)

print(output)
```

##### Output
```
{
 'my_first_name': 'Swetlana', 
 'location': 'Wolfratshausen'
}
```


---
## FictionaryLayer
Create Layers with custom fictions / vocabulary and use it on top of the standard set or as standalone.

Lets prepare some data we want to use in our new layer:
```
company_names = {
                 "IT": ["FastIT LLC", "wemakeIT Corp"],
                 "FinTech": ["QuickPay", "goNFC"]
                 }
```

Now let's create a new layer, add the company_names into the the layer and fuse it together with the standard fictionary
```
from fictionary import Fictionary, FictionaryLayer

layer = FictionaryLayer()
layer.add("company", company_names)

fn = Fictionary()
fn.fuse(layer)
```


You can now use the fictions from the layer within your fictionary.
```
output = fn.choose("company", "IT")
print(output)
```
Output: ``FastIT LLC``






---
## FictionaryTemplate
Use a template which will be filled with fictionary data.

You can add a json key name with ``--keyname`` where the fictional data will be stored.

##### Template "test.txt"
```
Hi, my name is {{firstname--myFirstName}} {{lastname:german}}. I live in {{street:spain}}, {{city:spain}}.
My cousin is {{firstname:slavik--cousinFirstName}} {{lastname:global}}. 
```


##### Syntax
```
from fictionary import Fictionary, FictionaryTemplate

fn = Fictionary()

template = FictionaryTemplate()

template.from_file("test.txt") 

output = template.generate(fn) # Can be used in reverse aswell: fn.generate(template)

print(output)
```


##### Output
```
{
 'json': {'myFirstName': 'Michael', 'cousinFirstName': 'Swetlana'}, 
 'text': 'Hi, my name is Michael Schmid. I live in Pla de Revoluzion 15-3-4, Lleida.\nMy cousin is Swetlana Alvarez. '
}
```

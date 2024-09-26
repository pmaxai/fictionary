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

```
from fictionary import Fictionary, FictionaryJson

fn = Fictionary()

my_element = FictionaryJson()

my_element.json = {
                    "my_first_name":"firstname:slavik",
                    "location":"city:germany"
                  }

output = fn.generate(my_element)

print(output)
```

Will result in output:
```
{
 'my_first_name': 'Swetlana', 
 'location': 'Wolfratshausen'
}
```

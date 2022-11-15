from PIL import Image
from os import chdir
from pathlib import Path

main_path = Path(__file__).parent.resolve()
chdir(main_path)

foo = Image.open("mirror.jpg")
print(foo.size)
foo_size = foo.size
foo = foo.resize((int(foo_size[0]/2),int(foo_size[1]/2)),Image.ANTIALIAS)
foo.save("mirror.jpg",quality=100)
print(foo.size)

#int(foo_size[0]*1.2)
#int(foo_size[1]*1.2)
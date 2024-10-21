# hydroponicGridGenerator

I have created this system for hydroponically growing plants in my aquarium. 

(insert a picture of the aquarium)

I really like the design, but modelling the stl files by hand, one by one, was quite time consuming and I did not 
always get the measures right the first time. So in case I or someone else wants to replicate this project, 
I have decided to create a script for generating all the necessary stl files all at once.

## The base implementation

The user gives width and length of their equivalent of aquarium, along with some other parameters. This will be significantly clearer once I add pictures showcasing the features the parameters affect.

### Features

- [x] Generate grid
  - [x] Lift edges (p)
- [x] Generate platform
  - [x] Move corners (p)
  - [x] Move "arms" (p)
  - [x] Round corners (p)
  - [x] edge height (p)
- [x] Margins
- [x] Calculate print counts
- [ ] Add "build up" pieces (.blend/stl)
- [ ] Add pots (.blend/stl)
- [x] Scale the end models

### Improve usability
- [x] GUI
- [x] Pictures
- [ ] Installation guide
- [ ] Installation scripts
- [x] Export as stl
- [x] Combined stl files
- [x] Better file management
- [x] Prefill values

### Advanced ideas

- [x] Generate test prints
- [ ] Custom plant holders
- [ ] Custom container shape
- [ ] Nozzle size input





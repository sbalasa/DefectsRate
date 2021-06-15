# DefectsRate
To calculate defect rate in production line fulfilment centers (FC) for quality control.


### Define Defect Rate
The term defect rate designates the portion of defective elements in relation to all items produced. The rate is deduced by dividing the number of defective elements by the number of non-defective elements

### Task
For this coding challenge we have prepared some sample data in the form of two csv’s
representing data coming from one FC. One of the files (data/input/picks/pick_1.csv)
contains pick events, the other file (data/input/quality_control/qc_1.csv) contains
information about which order (= box) and ingredient was checked and if it had a defect
or not.
We would like to know the defect rate per section over time.
It is your task to write an application which reads all input files, processes them and
outputs a csv file containing a dataset consisting of the defect rate, section and
timeframe.

### Solution Proposal
- The goal of the business is to have defect free orders, so orders placed by the customers are the prime factor in the production line. 

- The more the orders the more the profits, else less. Identifying defects for all the orders aren't practical so selected few are tested for quality control.

- `Defect Rate per order = (Defective Ingredients found per order / Total Picked Ingredients per order) in %`

- By calculating the defect rate with order_id as a base pointer provides us insights to determine the necessary business actions to avoid the defects. 

- Insights like, which order has highest defect rate, for what ingredients at which zones on what time.

- Based on these insights, necessary Business actions can be made to decrease the defect rate. 

- These analysis help the right project line manager to observe why certain ingredients are having defects or if there are any human errors in a particular zone etc.


## To prepare the Environment
`pip3 install -r requirements.txt`


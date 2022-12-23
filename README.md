# RESTAURANT OPERATIONS APP
#### Video Demo: <url>
#### Description:

This is a restaurant operations management and monitoring web app.

APP
----------------
Features :
- Point of sale (PoS) with item customization
- Kitchen order queue and customer customization tracker
- Monitor page for customer to see when their order is ready
- History page for past transactions data
- Price can be updated by admin user

Tech stack:
- Python
- Flask
- SQLite3


Login details:
- User password stored as a hash
- Werkzeug security is used to generate the hashed password
- User can change their password from the "Change Password" page


How to use:
The app divided into 4 main parts:
- Cashier (PoS)
- Kitchen
- Monitor
- History


After registering for an account, user can start adding order to the system


CASHIER
----------------
- To start ordering, user must input customer name from homepage then click ORDER button

- Click ADD button on the customer desired menu

- The selected menu can be customized using edit button in the cart

- The customization will be saved and passed to the cart

- Price difference will automatically be calculated in the cart total

- After order is completed, user must click SEND TO KITCHEN button to send the order to the kitchen page and tracker

Manual :
SEND TO KITCHEN will send the order to the kitchen tracker and complete the customer order

CLEAR CART this button will delete all items in the cart

CANCEL ORDER will clear the cart and clear the customer name from the system (to order again, user must enter customer name again from homepage)



KITCHEN
-----------------
Kitchen page displays order that have been sent to the kitchen. This page will refreshes itself every 5 seconds.

When the order is ready, the operator must click SERVE button to send the item to the monitor

Multiple orders with the same customer name can be completed by SERVE ALL button. This will send all orders with the same customer name to the monitor.

CANCEL button will cancel the order



MONITOR
-----------------
This page is intended to be display to customer side.

When order is ready, it will be shown in the monitor.

After the order is picked up by the customer (or served by the operator), COMPLETE button will remove the item from the monitor and give it COMPLETED status.

Multiple order for the same customer can be completed by clicking the red customer name. This will complete all the orders with the status ready for the same customer name.



History
-----------------
This page will show all completed order



Update Price
-----------------
To update the price the user must logged in using 'admin' username.

Default admin account -> username : admin, password: admin
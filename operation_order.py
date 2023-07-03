from model_order import Order
import random
import pandas as pd
import time 
import numpy as np
import string
from model_user import User
from operation_user import UserOperation
from operation_customer import CustomerOperation
from opreation_product import ProductOperation
from model_product import Product
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#%%
class OrderOperation:
    
    prod_df = Product().read_return_df(is_string= False)
    prod_df_id_list = prod_df["prod_id"].tolist()
    def generate_unique_order_id(
        self
    ) -> str :
        """
        generates unique 6 digit order_id and returns

        Returns
        -------
        str
            DESCRIPTION.

        """
        start = (10**(5-1))
        end = (10**5)-1
        flag = True
        while flag: 
            temp_order_id = "o_"+str(random.randint(start, end))
            order_df = Order().read_return_df()
            try: 
                df_exist_order_id = pd.Series(order_df["order_id"])
            except KeyError : 
                df_exist_order_id = pd.Series([],dtype= "str")
            if temp_order_id not in df_exist_order_id.values:
                flag = False
                return temp_order_id
            else:
                flag = True
                continue

#%%    
    def create_an_order(
        self,
        customer_id: str,
        product_id: str,
        order_time: str = Order().current_time_str()
        ) -> bool :
        """
        creates an order and writes it into orders txt

        Parameters
        ----------
        customer_id : str
            DESCRIPTION.
        product_id : str
            DESCRIPTION.
        order_time : str, optional
            DESCRIPTION. The default is current_time_str().

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if product_id not in OrderOperation().prod_df_id_list : 
            return False
        Order.order_id = self.generate_unique_order_id()
        Order.user_id = customer_id
        Order.prod_id = product_id
        Order.order_time = order_time
        order_obj = Order(Order.order_id,Order.user_id,Order.prod_id,
                          Order.order_time)
        order_obj_df = pd.DataFrame(order_obj.__dict__ , index = [0])
        return Order().append_to_file(order_obj_df)
#%%

    def delete_order(
        self,
        order_id
    ) -> bool : 
        """
        searches if order_id exists if it doesnt then returns False
        else deletes it from file

        Parameters
        ----------
        order_id : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        curr_order_df = Order().search_return_df(search_term = order_id, 
                                                 is_order_id = True,
                                                 is_cust_id = False)
        if curr_order_df.empty : 
            return False
        else : 
            pass
        
        order_file_df = Order().read_return_df()
        try: 
            del_file_df = order_file_df.drop(curr_order_df.index)
            return Order().write_df_to_file(del_file_df)
        except: 
            return False
#%% 
    def order_obj(row) : 
        return Order(**row["order_dict"])

#%%

    def get_order_list(
        self,
        customer_id:str,
        page_number:str,
        ) -> tuple() : 
        """
        get customer order lists

        Parameters
        ----------
        customer_id : str
            DESCRIPTION.
        page_number : str
            DESCRIPTION.
         : TYPE
            DESCRIPTION.

        Returns
        -------
        tuple
            DESCRIPTION.

        """
        
        if page_number in ("", None): 
            page_number = "0"
            
        order_find = Order().search_return_df(search_term = customer_id, 
                                              is_order_id = False, 
                                              is_cust_id = True)
        page_size = 10
        page_nums = np.arange(len(order_find)) // page_size + 1
        order_find["page_num"] = page_nums 
        max_pages = order_find["page_num"].max()
        if np.isnan(max_pages) : 
            max_pages = "0"
        page_number = int(page_number)
        return_df = order_find.query("page_num == @page_number")
        return_df = return_df.drop("page_num",axis = 1)
        order_df_dict = return_df.to_dict("records")
        order_return_df = pd.DataFrame()
        order_return_df["order_dict"] = order_df_dict
        order_return_df["order_obj"] = order_return_df.apply(
                OrderOperation.order_obj,axis = 1)
        order_return_df = order_return_df.drop("order_dict",axis = 1)
        return_order_list = order_return_df["order_obj"].to_list()
        return_tuple = (return_order_list,str(page_number),max_pages)
        return return_tuple
            
#%%

    def generate_test_order_data(
        self 
        ) -> bool :
        """
        creates and writes new customers and orders

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        try : 
            def generate_random_email():
                username = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
                domain = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
                extension = random.choice(['com', 'net', 'org', 'edu'])
                email = f"{username}@{domain}.{extension}"
                return email
            
            email_ids = []  
            for _ in range(10):
                email = generate_random_email()
                email_ids.append(email)
                
            password = "password123"
            password_list = [password]*10
            password_encrypt_list = password_list
            
            user_file_df = User().read_return_df(User.user_file_path)
            existing_usernames = set(user_file_df[User.user_name])
    
            new_usernames = []
            for _ in range(10):
                while True:
                    username = (''.join(random.choice(string.ascii_lowercase + '_') 
                                        for _ in range(random.randint(6, 10))))
                    if username not in existing_usernames:
                        existing_usernames.add(username)
                        break
                new_usernames.append(username)
            
            mobile_num = []
            for _ in range(10):
                start_with = random.choice(["03", "04"])
                numbers = [start_with] + [str(random.randint(0, 9)) for _ in range(8)]
                number_string = ''.join(numbers)
                mobile_num.append(number_string)
                
            user_data = {
                User.user_name : new_usernames,
                User.user_password : password_encrypt_list,
                User.user_email : email_ids,
                User.user_mobile: mobile_num
                }
            
            user_file_col = [User.user_name,User.user_password,User.user_email,User.user_mobile]
            df_new_user = pd.DataFrame(user_data,columns=user_file_col)
            df_new_dict = df_new_user.to_dict("records")
            
            #writing/ regestering this new users
            for elem in df_new_dict : 
                CustomerOperation().register_customer(**elem)
            
            # retrive these new users data frame 
            updated_user_df = User().read_return_df(User.user_file_path)
            
            updated_user_df = updated_user_df[
                updated_user_df[User.user_name].isin(new_usernames)]
            #product data frame
            prod_df = Product().read_return_df()
                
            for _, user_row in updated_user_df.iterrows():
                cust_id = user_row[User.user_id]
                num_orders = random.randint(50, 200)
                
                for _ in range(num_orders):
                    prod_id = random.choice(prod_df['prod_id'])
                    order_time = Order().random_time_str()
                    OrderOperation().create_an_order(customer_id = cust_id, 
                                         product_id = prod_id,
                                         order_time= order_time)
            return True
        except : 
            return False

#%%    

    def delete_all_orders(
        self
    ) -> None :
        """
        deletes entire data from orders.txt 

        Returns
        -------
        None
            DESCRIPTION.

        """
        del_prod = pd.DataFrame()
        return Order().write_df_to_file(del_prod)
#%%
    def generate_single_customer_consumption_figure(self, customer_id):
        """
        this generates a plot for customer and returns false 

        Parameters
        ----------
        customer_id : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        try:
            
            df = Order().read_return_df(is_string=False)
            orders = df[df["user_id"] == customer_id]
            if orders.empty : 
                return False
            
            merged_df = orders.merge(
                OrderOperation().prod_df[["prod_id","prod_current_price"]], 
                on="prod_id", how="left")
            
            merged_df["order_month"] = pd.to_datetime(merged_df["order_time"]).dt.month
            monthly_consumption = merged_df.groupby(
                "order_month")["prod_current_price"].sum()
            
            colors = ["#993333", "#994C33", "#996633", "#998033", "#6C9933", 
                      "#339933", "#339966", "#336699","#334C99", "#333399", 
                      "#663399", "#993366"]
            plt.figure(figsize=(14, 9))
            plt.bar(monthly_consumption.index, monthly_consumption.values,
                    color=colors)
            plt.xlabel("Month")
            plt.ylabel("Consumption")
            plt.title(f"Monthly Consumption for Customer {customer_id}")
            plt.xticks(monthly_consumption.index, 
                       ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                        "Sep", "Oct", "Nov", "Dec"])
            plt.savefig("data/figure/single_customer_consumption_chart.png")
            plt.close()
            return True
        except : 
            return False
#%%
    def generate_all_customers_consumption_figure(self) : 
        """
        All customers consumption figure

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        try : 
            df = Order().read_return_df(is_string=False)
            if df.empty : 
                return False
            merged_df = df.merge(
                OrderOperation().prod_df[["prod_id","prod_current_price"]], 
                on="prod_id", how="left")
            merged_df["order_month"] = pd.to_datetime(merged_df["order_time"]).dt.month
            monthly_consumption = merged_df.groupby("order_month")["prod_current_price"].sum()
        
            colors = ["#993333", "#994C33", "#996633", "#998033", "#6C9933", 
                      "#339933", "#339966", "#336699","#334C99", "#333399", 
                      "#663399", "#993366"]
            
            plt.figure(figsize=(15, 8))
            plt.bar(monthly_consumption.index, monthly_consumption.values,
                    color= colors)
            plt.xlabel("Month")
            plt.ylabel("Consumption")
            plt.title("Monthly Consumption for All Customers")
            plt.xticks(monthly_consumption.index, ["Jan", "Feb", "Mar", "Apr", 
                                                   "May", "Jun", "Jul", "Aug", 
                                                   "Sep", "Oct", "Nov", "Dec"])
        
    
            plt.savefig("data/figure/all_customers_consumption_figure.png")
            plt.close()
            return True
        except : 
            return False
#%%

    def generate_all_top_10_best_sellers_figure(self):
        """
        a graph to show the top 10 best-selling products and sort
        the result in descending order

        Returns
        -------
        None.

        """
        
        try :
            
            order_df = Order().read_return_df(is_string=False)
            if order_df.empty : 
                return False 
            
            top_sellers = order_df.groupby(
                "prod_id")["order_id"].count().sort_values(ascending=False)
            top_10_sellers = top_sellers.head(10)
            colors = ["#993333", "#994C33", "#996633", "#998033", "#6C9933", 
                      "#339933", "#339966", "#336699","#334C99", "#333399", 
                      "#663399", "#993366"]
            
            plt.figure(figsize=(15, 8))
            plt.bar(top_10_sellers.index, 
                    top_10_sellers.values,color = colors)
            
            plt.xlabel("Product ID")
            plt.ylabel("Quantity Sold")
            plt.title("Top 10 Best-Selling Products")
            plt.xticks(rotation=45)
         
            # Save the figure to the data/figure folder
            plt.savefig("data/figure/all_top_10_best_sellers_chart.png")
            plt.close()
            return True 
        except : 
            return False
#%%        
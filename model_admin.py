from model_user import User
"""
This class is the main class for admins they are initialized and handled

Name: Pavan Ramesh Nargund
Student Id: 33503575
Create date: 30-05-2023
Final date: 30-05-2023

"""

class Admin(User):
    
    def __init__(
        self,
        user_id: str = User.default_user_id,
        user_name: str = User.default_user_name,
        user_password: str = User.default_user_password,
        user_register_time: str = User.default_register_time,
        user_role: str = User.admin_role
    ):
        """
        Initalizing admin instances; overriding init

        Parameters
        ----------
        user_id : str, optional
            DESCRIPTION. The default is User.default_user_id.
        user_name : str, optional
            DESCRIPTION. The default is User.default_user_name.
        user_password : str, optional
            DESCRIPTION. The default is User.default_user_password.
        user_register_time : str, optional
            DESCRIPTION. The default is User.default_register_time.
        user_role : str, optional
            DESCRIPTION. The default is User.admin_role.

        Returns
        -------
        None.

        """
        super().__init__(user_id,user_name,user_password,user_register_time,\
                       user_role)
        
    def __str__(
        self
    )->str:
        """
        specific way of printing instances 

        Returns
        -------
        str
            DESCRIPTION.

        """
        return super().__str__()
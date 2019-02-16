"""
Created: 2/9/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""


class UserPermissions:
    READ = 1
    WRITE = 10
    UPDATE = 20
    CREATE = 30
    DELETE = 40
    MANAGE = 50
    TRANSFER_TO = 60
    TRANSFER_FROM = 70

    EMPLOYEE = 100
    EMPLOYEE_ADMIN = 200


class BasicUserRoles:
    USER = [UserPermissions.READ, UserPermissions.WRITE, UserPermissions.CREATE,
            UserPermissions.DELETE, UserPermissions.MANAGE,
            UserPermissions.TRANSFER_TO, UserPermissions.TRANSFER_FROM]

    EMPLOYEE = [UserPermissions.READ, UserPermissions.WRITE, UserPermissions.CREATE,
                UserPermissions.DELETE, UserPermissions.MANAGE,
                UserPermissions.TRANSFER_TO, UserPermissions.TRANSFER_FROM,
                UserPermissions.EMPLOYEE]

    EMPLOYEE_SUPER_ADMIN = [UserPermissions.READ, UserPermissions.WRITE, UserPermissions.CREATE,
                            UserPermissions.DELETE, UserPermissions.MANAGE,
                            UserPermissions.TRANSFER_TO, UserPermissions.TRANSFER_FROM,
                            UserPermissions.EMPLOYEE, UserPermissions.EMPLOYEE_ADMIN]

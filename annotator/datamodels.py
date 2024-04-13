drivings_schema = '''
{
    "pages": [1],  # visible pages of a document, fixed
    "class_of_document": "driver license",  # name of document class, fixed
    "last_name_ru": str,  # last name in Russian
    "first_name_ru": str,  # first name in Russian
    "middle_name_ru": str,  # middle name in Russian
    "last_name_en": str,  # last name in English
    "first_name_en": str,  # first name in English
    "middle_name_en": str,  # middle name in English
    "birth_date": str,  # birth date in DD.MM.YYYY
    "birth_place_ru": str,  # where owner was born in Russian
    "birth_place_en": str,  # where owner was born in English
    "issued": str,  # date of an issue in DD.MM.YYYY format
    "expire: str,  # date of expiration in DD.MM.YYYY format
    "department_code": str,  # identifier of GIBDD issued document
    "id": str,  # unique identifier of the document
    "living_ru": str,  # where owner living in Russian
    "living_en": str,  # where owner living in English
    "categories": List[str],  # list of allowed vehicle categories
    "experience": str,  # year since driving experience started
}
'''

pass_schema = '''
{
    "pages": [2,3],  # visible pages of a document, fixed
    "class_of_document": "citizen's passport",  # name of document class, fixed
    "gender": str,  # gender of a person, one of ["female", "male"]
    "last_name": str,  # last name in Russian
    "first_name": str,  # first name in Russian
    "middle_name": str,  # middle name in Russian
    "birth_date": str,  # birth date in DD.MM.YYYY
    "birth_place": str,  # self explained
    "where": str  # where, document was issued
    "department_code": str,  # identifier of department issued document
    "id": str,  # unique identifier of the document
    "issued": str,  # date of an issue in DD.MM.YYYY format
}
'''


sts_schema = '''
{
    "pages": [1],  # visible pages of a document, fixed
    "class_of_document": "certificat d'immatriculation",  # name of document class, fixed 
    "id": str,  # unique identifier of the document (full string in red color)
    "last_name_ru": str,  # owner last name in Russian
    "first_name_ru": str,  # owner first name in Russian
    "middle_name_ru": str,  # owner middle name in Russian
    "last_name_en": str,  # owner last name in English
    "first_name_en": str,  # owner first name in English
    "address": str,  # адресс: город, улица, дом, квартира
    "special_marks": str,  # Особые отметки 
    "department_code": str,  # код подразделения ГИБДД  
    "regid": str,  # государственный регистрационный номер
    "vin": str,  # идентификационный номер (VIN)
    "mark": str,  # марка
    "model": str,  # модель
    "type": str,  # тип ТС
    "category": str,  # категория ТС
    "issue_year": str,  # год выпуска ТС
    "chassis": str,  # номер шасси (рама)
    "body": str,  # номер кузова
    "color": str,  # цвет
    "approval": str,  # номер одобрения
    "ecology_class": str,  # экологический класс
    "раssport": str,  # номер техпаспорта
    "max_weight_kg": str,  # технически допустимая максимальная масса, кг
    "weight_kg": str,  # масса в снаряженном состоянии, кг
}
'''

pts_schema = '''
{
    "pages": [1],  # visible pages of a document, fixed
    "class_of_document": "vehicle passport",  # name of document class, fixed
    "id": str,  # unique identifier of the document (full string in red color)
    "vin": str, # идентификационный номер (VIN)
    "mark": str,  # марка, модель ТС
    "name": str,  # наименование (тип ТС)
    "category": str,  # категория ТС
    "issue_year": str,  # год изготовления ТС
    "model": str,  # модель
    "engine_id": str,  # № двигателя
    "chassis": str,  # шасси (рама) №
    "body": str,  # кузов (кабина, прицеп) №
    "color": str,  # цвет
    "engine_power": str,  # мощность двигателя, л. с. (кВт)
    "engine_volume": int,  # рабочий объем двигателя, куб.см
    "engine_type": str,  # тип двигателя
    "ecology_class": str,  # экологический класс
    "max_weight_kg": str,  # разрешенная максимальная масса, кг
    "weight_kg": str,  # масса без нагрузки, кг
    "manufacturer": str,  # организация - изготовитель ТС (страна)
    "approval": str,  # номер одобрения
    "export_country": str,  # страна вывоза ТС
    "seria": str,  # серия, № ТД, ТПО
    "restrictions": str,  # таможенные ограничения  
    "owner": str, # наименование (ф. и. о.) собственника ТС
    "address": str, # адресс собственника ТС
    "department_name": str,  # наименование организации, выдавшей паспорт
    "department_address": str,  # адрес организации, выдавшей паспорт
    "issue_date": str,  # дата выдачи пасспорта
    "special marks": str,  # особые отметки 
}
'''
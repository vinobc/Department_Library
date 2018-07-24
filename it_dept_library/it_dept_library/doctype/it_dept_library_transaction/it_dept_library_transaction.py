from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ITDeptLibraryTransaction(Document):
     def validate(self):
        last_transaction = frappe.get_list("IT Dept Library Transaction",
            fields=["type", "date"],
            filters = {
                "book": self.book,
                "date": ("<=", self.date),
                "name": ("!=", self.name)
            })
        if self.type=="Issue":
            msg = _("Book {0} {1} has not been returned since {2}")
            if last_transaction and last_transaction[0].type=="Issue":
                frappe.throw(msg.format(self.book, self.book_name,
                    last_transaction[0].date))
        else:
            if not last_transaction or last_transaction[0].type!="Issue":
                frappe.throw(_("Cannot return book not issued"))


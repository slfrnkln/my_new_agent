from typing import List
import os, sys

from oef.query import Eq, Range, Constraint, Query, AttributeSchema
from oef.schema import DataModel, Description , Location


class TIME_AGENT (DataModel):
	ATTRIBUTE_TIMEZONE = AttributeSchema("timezone", int, True, "TimeZone")
	ATTRIBUTE_ID = AttributeSchema("id", str, True, "Id")
	ATTRIBUTE_TWENTYFOUR = AttributeSchema("twentyfour", bool, False, "If the clock is twentyfour hour" )


	def __init__(self):
		super().__init__("time_datamodel",[self.ATTRIBUTE_TIMEZONE,
									  	 			 self.ATTRIBUTE_ID, self.ATTRIBUTE_TWENTYFOUR],
									  	 			 "Agent has the time.")

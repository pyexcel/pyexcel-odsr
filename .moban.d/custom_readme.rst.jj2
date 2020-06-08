{%extends 'README.rst.jj2' %}

{%block documentation_link%}
{%endblock%}

{%block description%}
**pyexcel-odsr** is a specialized ods reader based on tailored ods reader from
`messytables <https://github.com/okfn/messytables>`_.
You are likely to use it with `pyexcel <https://github.com/pyexcel/pyexcel>`_.
Differring from `pyexcel-ods <https://github.com/pyexcel/pyexcel-ods>`_ and
`pyexcel-ods3 <https://github.com/pyexcel/pyexcel-ods3>`_ in handling ods file, this
library could read partial content from a huge ods file.

{%endblock%}

{% block write_to_file %}

.. testcode::
   :hide:

    >>> from pyexcel_ods import save_data
    >>> data = OrderedDict() # from collections import OrderedDict
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
    >>> save_data("your_file.{{file_type}}", data)

{% endblock %}


{% block write_to_memory %}

.. testcode::
   :hide:

    >>> data = OrderedDict()
    >>> data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
    >>> data.update({"Sheet 2": [[7, 8, 9], [10, 11, 12]]})
    >>> io = StringIO()
    >>> save_data(io, data)
    >>> unused = io.seek(0)
    >>> # do something with the io
    >>> # In reality, you might give it to your http response
    >>> # object for downloading


{%endblock%}

{% block pyexcel_write_to_file%}

.. testcode::
   :hide:

    >>> sheet.save_as("another_file.{{file_type}}")

{% endblock %}

{% block pyexcel_write_to_memory%}
{% endblock %}

{%block extras %}
Credits
================================================================================

This library is based on the ods of messytables, Open Knowledge Foundation Ltd.

{%endblock%}

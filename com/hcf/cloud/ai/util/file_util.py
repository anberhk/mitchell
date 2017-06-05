# -*- coding: utf-8 -*-
"""
    Author: huangkun
    file_util is use to deal file, include split、upoload、and some other action
"""

import os
import datetime
import uuid

from com.hcf.cloud.ai.constant import http_consts
from com.hcf.cloud.ai.constant import path_consts
from com.hcf.cloud.ai.constant import file_consts
from com.hcf.cloud.ai.constant import str_consts
from com.hcf.cloud.ai.constant import number_consts


def split_upload_file(upload_file):
    """
    split a file by file boundary, this file is composed by multiple min file

    Parameters:
        upload_file - this is upload multiple file
    Returns:
    """
    if (upload_file is not None and
            os.path.exists(upload_file)):
        fo = open(upload_file)
        fo_output = None
        boundary_data = []
        line_count = number_consts.ONE
        boundary_start_line_count = number_consts.ZERO
        boundary_end_line_count = number_consts.ZERO
        boundary_begin_line = None
        boundary_end_line = http_consts.FILE_BOUNDARY

        for line in fo:
            line = line.strip()
            # get start line of one chunk
            if line_count == number_consts.ONE:
                boundary_begin_line = line
                boundary_start_line_count = number_consts.ONE

            # get start line number of one chunk
            if line.find(boundary_begin_line) != number_consts.NEGATIVE_ONE:
                boundary_start_line_count = line_count
                boundary_end_line_count = number_consts.ZERO

            # find the end character of chunk
            if line.find(boundary_end_line) != number_consts.NEGATIVE_ONE:
                chunk = "".join(boundary_data)
                input_name, source_file_name = get_file_name_from_chunk(chunk)
                store_path = None
                if (source_file_name is not None
                    and len(source_file_name) > number_consts.ZERO):
                    source_file_name, new_file_name = generate_file_name(source_file_name)
                    store_path = os.path.join(generate_file_path(), new_file_name)

                if fo_output is not None:
                    if not fo_output.closed:
                        fo_output.close()
                if len(store_path) > number_consts.ZERO:
                    fo_output = open(store_path, 'a')
                else:
                    fo_output = None
                boundary_end_line_count = line_count
                boundary_data = []

            # judge the end of boundary if exists or not
            if boundary_end_line_count == number_consts.ZERO:
                boundary_data.append(line)
            else:
                if line_count <= boundary_start_line_count <= boundary_end_line_count:
                        boundary_data.append(line)
                else:
                    if (len(line) > number_consts.ZERO and
                                fo_output is not None and
                                line_count > boundary_end_line_count):
                        fo_output.write(line + str_consts.BR)
            line_count += number_consts.ONE


def get_file_name_from_chunk(boundary):
    """
    get file name from single file

    Parameters:
        param boundary - this is a file chunk

    Returns:
        the name of file
    """
    file_name_start_idx = boundary.find(str_consts.FILE_NAME)
    file_name_end_idx = boundary.rfind(str_consts.BACKQUOTE) #;
    file_name_start_idx = file_name_start_idx + number_consts.TEN
    file_name = boundary[file_name_start_idx:file_name_end_idx]

    input_name_start_idx = boundary[number_consts.ZERO:file_name_start_idx].rfind(file_consts.str_consts.INPUT_FILE_NAME)
    input_name_end_idx = boundary[number_consts.ZERO:file_name_start_idx].rfind(str_consts.BACKQUOTE + str_consts.JUMPER) # ";
    input_name_start_idx = input_name_start_idx + number_consts.SIX
    ipnut_name = boundary[input_name_start_idx:input_name_end_idx]
    return ipnut_name, file_name


def generate_file_path():
    """
    generate store path by current date

    Returns:
        return new path like E:/upload/2017/06/01/
    """
    store_array = []
    today = datetime.datetime.now()

    store_array.append(str(today.year))
    store_array.append(str(today.month))
    store_array.append(str(today.day))

    new_sub_path = os.sep.join(store_array)
    new_path = os.path.join(path_consts.FILE_UPLOAD_DIR, new_sub_path)
    return new_path


def generate_file_name(source_name):
    """
    generate new filename by sepecial rule

    Parameters:
        param source_name - the name of source file
    Returns:
        return new file name (uuid+suffix)
    """
    new_file_name = None
    if source_name is not None:
        ext_start_idx = source_name.rfind(str_consts.SPOT)
        ext = source_name[ext_start_idx:len(source_name)]
        name_prefix = uuid.UUID
        new_file_name = str(name_prefix).join(ext)
    return source_name, new_file_name

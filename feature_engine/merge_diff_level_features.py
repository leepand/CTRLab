######不同的libsvm数据合并,new_add数据的index自动在base基础上递增
from six import iteritems, PY2, PY3, string_types, text_type

def safe_float(text, replace_dict=None):
    """
    Attempts to convert a string to an int, and then a float, but if neither is
    possible, just returns the original string value.
    :param text: The text to convert.
    :type text: str
    :param replace_dict: Mapping from text to replacement text values. This is
                         mainly used for collapsing multiple labels into a
                         single class. Replacing happens before conversion to
                         floats. Anything not in the mapping will be kept the
                         same.
    :type replace_dict: dict from str to str
    """

    # convert to text to be "Safe"!
    text = text_type(text)

    if replace_dict is not None:
        if text in replace_dict:
            text = replace_dict[text]
        else:
            logging.getLogger(__name__).warning('Encountered value that was '
                                                'not in replacement '
                                                'dictionary (e.g., class_map):'
                                                ' {}'.format(text))
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text.decode('utf-8') if PY2 else text
        except TypeError:
            return 0.0
    except TypeError:
        return 0
#print safe_float('g23e')
def _pair_to_tuple(pair, feat_map=None):
    """
    Split a feature-value pair separated by a colon into a tuple.  Also
    do safe_float conversion on the value.
    """
    name, value = pair.split(':')
    if feat_map is not None:
        name = feat_map[name]
    value = safe_float(value)
    name = safe_float(name)+100
    return (name, value)
#print _pair_to_tuple('g23e:1')
import time
######sort key first using code:big_file_sort

from __future__ import print_function, unicode_literals
from collections import OrderedDict ## sort new feature index 
'''
import big_file_sort
input_file='userid_app_doclevel_vectors.txt'
output_file ='userid_app_doclevel_vectors.sorted'
big_file_sort.sort_file(input_file, output_file)
input_file2='userid_search_vectors2.txt'
output_file2 ='userid_search_vectors2.sorted'
big_file_sort.sort_file(input_file2, output_file2)
'''

def mergeLine(base,new_add):
    return 'lipd'
def mergeFile(file_base,file_new_add,file_merge):
    start=time.clock()
    fp_base = open(file_base,"r")
    fp_new_add = open(file_new_add,"r")
    fp_merge = open(file_merge,"w")

    base_line = fp_base.readline()
    new_add_line = fp_new_add.readline()
    
    while base_line and new_add_line:
        base = base_line.strip().split()
        new_add = new_add_line.strip().split()

        if base[0] < new_add[0]:
            fp_merge.write(base_line)
            base_line = fp_base.readline()
        elif base[0] > new_add[0]:
            new_add_match=new_add[1:]
            curr_info_dict = dict(_pair_to_tuple(pair, feat_map=None) for pair in new_add_match)
            curr_info_dict = OrderedDict(sorted(curr_info_dict.items(),key = lambda t:t[0]))
            print('{}'.format(new_add[0]), end=' ', file=fp_merge)
            print(' '.join(('{}:{}'.format(field, value) for field, value in curr_info_dict.iteritems())) ,end='\n', file=fp_merge)
            #fp_merge.write(new_add_line)
            new_add_line = fp_new_add.readline()
        else:     
            #megre_line = mergeLine(base,new_add)
            new_add_match=new_add[1:]
            curr_info_dict = dict(_pair_to_tuple(pair, feat_map=None) for pair in new_add_match)
            curr_info_dict = OrderedDict(sorted(curr_info_dict.items(),key = lambda t:t[0]))
            print('{}'.format(base[0]), end=' ', file=fp_merge)
            print('{}'.format(' '.join(base[1:])), end=' ', file=fp_merge)
            #fp_merge.write(megre_line+'\n')
            print(' '.join(('{}:{}'.format(field, value) for field, value in curr_info_dict.iteritems())) ,end='\n', file=fp_merge)
            #fp_merge.write(megre_line+'\n')
            base_line = fp_base.readline()
            new_add_line = fp_new_add.readline()
            continue
        
    if base_line:
        fp_merge.write(base_line)
        for line in fp_base:
            fp_merge.write(line)
    if new_add_line:
        fp_merge.write(new_add_line)
        for line in fp_new_add:
            fp_merge.write(line)  
            
    fp_merge.close()
    fp_base.close()
    fp_new_add.close()
    end=time.clock()
    print("Running time: %s seconds"%(end-start))
#mergeFile('./transform_data/app/userid_app_doclevel_vectors.txt','./transform_data/userid_search_vectors2.txt','merge2.txt')
#mergeFile('./1.txt','./2.txt','merge2.txt')
mergeFile('./userid_search_vectors2.sorted','./userid_app_doclevel_vectors.sorted','merge_search-app_info.libsvm')
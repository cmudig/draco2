from draco import is_satisfiable
from draco.asp_utils import Block
from draco.programs import define, hard, helpers


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,text).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).

    :- violation(_).
    """
    )


def test_text_channel_without_text_mark():
    b = hard.blocks["text_channel_without_text_mark"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).

    :- violation(_).
    """
    )


def test_bin_and_aggregate():
    b = hard.blocks["bin_and_aggregate"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    entity(encoding,root,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).

    :- violation(_).
    """
    )


def test_no_encodings():
    b = hard.blocks["no_encodings"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).
    entity(encoding,1,2).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(mark,root,3).

    :- violation(_).
    """
    )


def test_repeat_channel():
    b = hard.blocks["repeat_channel"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,y).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(scale,root,3).
    attribute((scale,channel),3,x).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    entity(encoding,1,3).
    attribute((encoding,channel),3,y).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).

    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    entity(encoding,1,3).
    attribute((encoding,channel),3,x).

    :- violation(_).
    """
    )


def test_encoding_no_field_and_not_count():
    b = hard.blocks["encoding_no_field_and_not_count"]
    assert isinstance(b, Block)
    p = b.program
    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,field),1,temp).
    attribute((encoding,aggregate),1,mean).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).

    :- violation(_).
    """
    )


def test_count_with_field():
    b = hard.blocks["count_with_field"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute((encoding,aggregate),1,count).
    attribute((encoding,field),1,temp).

    :- violation(_).
    """
    )


def test_point_tick_bar_without_x_or_y():
    b = hard.blocks["point_tick_bar_without_x_or_y"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((mark,type),1,tick).
    attribute((encoding,channel),1,x).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((mark,type),1,tick).

    :- violation(_).
    """
    )

# == Stacking ==

def test_stack_without_bar_area():
    b = hard.blocks["stack_without_bar_area"]
    assert isinstance(b, Block)
    p = helpers.program + b.program

    assert is_satisfiable(
        p
        + """
    entity(mark,root,2).
    attribute((mark,type),2,bar).
    entity(encoding,2,3).
    attribute((encoding,channel),3,x).
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,zero).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(mark,root,2).
    attribute((mark,type),2,area).
    entity(encoding,2,3).
    attribute((encoding,channel),3,x).
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,normalize).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,2).
    attribute((mark,type),2,point).
    entity(encoding,2,3).
    attribute((encoding,channel),3,x).
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,normalize).

    :- violation(_).
    """
    )

def test_stack_without_summative_agg():
    b = hard.blocks["stack_without_summative_agg"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    attribute((encoding,stack),3,zero).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,mean).

    :- violation(_).
    """
    )

def test_no_stack_with_bar_area_discrete_color():
    b = hard.blocks["no_stack_with_bar_area_discrete_color"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(field,root,1).
    attribute((field,name),1,wind).
    attribute((field,type),1,number).
    entity(field,root,2).
    attribute((field,name),2,condition).
    attribute((field,type),2,string).
    entity(mark,root,3).
    attribute((mark,type),3,point).
    entity(encoding,3,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,field),4,temperature).
    entity(encoding,3,5).
    attribute((encoding,channel),5,y).
    attribute((encoding,field),5,wind).
    entity(encoding,3,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,7).
    attribute((scale,channel),7,x).
    attribute((scale,type),7,linear).
    entity(scale,root,8).
    attribute((scale,channel),8,y).
    attribute((scale,type),8,linear).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,ordinal).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(field,root,1).
    attribute((field,name),1,wind).
    attribute((field,type),1,number).
    entity(field,root,2).
    attribute((field,name),2,condition).
    attribute((field,type),2,string).
    entity(mark,root,3).
    attribute((mark,type),3,bar).
    entity(encoding,3,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,field),4,temperature).
    entity(encoding,3,5).
    attribute((encoding,channel),5,y).
    attribute((encoding,field),5,wind).
    attribute((encoding,stack),5,zero).
    attribute((encoding,aggregate),5,sum).
    entity(encoding,3,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,7).
    attribute((scale,channel),7,x).
    attribute((scale,type),7,linear).
    entity(scale,root,8).
    attribute((scale,channel),8,y).
    attribute((scale,type),8,linear).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,ordinal).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(field,root,1).
    attribute((field,name),1,wind).
    attribute((field,type),1,number).
    entity(field,root,2).
    attribute((field,name),2,condition).
    attribute((field,type),2,string).
    entity(mark,root,3).
    attribute((mark,type),3,area).
    entity(encoding,3,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,field),4,temperature).
    entity(encoding,3,5).
    attribute((encoding,channel),5,y).
    attribute((encoding,field),5,wind).
    entity(encoding,3,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,7).
    attribute((scale,channel),7,x).
    attribute((scale,type),7,linear).
    entity(scale,root,8).
    attribute((scale,channel),8,y).
    attribute((scale,type),8,linear).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,ordinal).

    :- violation(_).
    """
    )

def test_stack_without_discrete_color_or_detail():
    b = hard.blocks["stack_without_discrete_color_or_detail"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,ordinal).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,6).
    attribute((encoding,channel),6,detail).
    attribute((encoding,field),6,condition).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,linear).

    :- violation(_).
    """
    )

def test_stack_detail_without_q_color():
    b = hard.blocks["stack_detail_without_q_color"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,5).
    attribute((encoding,channel),4,detail).
    entity(encoding,2,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,5).
    attribute((encoding,channel),4,detail).

    :- violation(_).
    """
    )

def test_stack_detail_without_q_color_2():
    b = hard.blocks["stack_detail_without_q_color_2"]
    assert isinstance(b, Block)
    p = b.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,5).
    attribute((encoding,channel),4,detail).
    entity(encoding,2,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    attribute((encoding,aggregate),6,sum).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).
    entity(encoding,2,5).
    attribute((encoding,channel),4,detail).
    entity(encoding,2,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).

    :- violation(_).
    """
    )

def test_stack_discrete():
    b = hard.blocks["stack_discrete"]
    assert isinstance(b, Block)
    p = b.program + helpers.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    attribute((encoding,aggregate),4,sum).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    entity(scale,root,6).
    attribute((scale,channel),6,x).
    attribute((scale,type),6,ordinal).

    :- violation(_).
    """
    )

    # dont know why doesnt work
    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).
    attribute((encoidng,binning),4,20).

    :- violation(_).
    """
    )

def test_stack_without_x_y():
    b = hard.blocks["stack_without_x_y"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,stack),4,zero).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,color).
    attribute((encoding,stack),4,zero).

    :- violation(_).
    """
    )

def test_stack_with_non_positional_non_agg():
    b = hard.blocks["stack_with_non_positional_non_agg"]
    assert isinstance(b, Block)
    p = b.program + define.program + helpers.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(field,root,1).
    attribute((field,name),1,wind).
    attribute((field,type),1,number).
    entity(field,root,2).
    attribute((field,name),2,condition).
    attribute((field,type),2,string).
    entity(mark,root,3).
    attribute((mark,type),3,point).
    entity(encoding,3,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,field),4,temperature).
    entity(encoding,3,5).
    attribute((encoding,channel),5,y).
    attribute((encoding,field),5,wind).
    attribute((encoding,stack),5,zero).
    attribute((encoding,aggregate),5,sum).
    entity(encoding,3,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,7).
    attribute((scale,channel),7,x).
    attribute((scale,type),7,linear).
    entity(scale,root,8).
    attribute((scale,channel),8,y).
    attribute((scale,type),8,linear).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,ordinal).

    :- violation(_).
    """
    )

    # dont know why doesnt work
    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(field,root,1).
    attribute((field,name),1,wind).
    attribute((field,type),1,number).
    entity(field,root,2).
    attribute((field,name),2,condition).
    attribute((field,type),2,string).
    entity(mark,root,3).
    attribute((mark,type),3,point).
    entity(encoding,3,4).
    attribute((encoding,channel),4,x).
    attribute((encoding,field),4,temperature).
    entity(encoding,3,5).
    attribute((encoding,channel),5,y).
    attribute((encoding,field),5,wind).
    attribute((encoding,stack),5,zero).
    entity(encoding,3,6).
    attribute((encoding,channel),6,color).
    attribute((encoding,field),6,condition).
    entity(scale,root,7).
    attribute((scale,channel),7,x).
    attribute((scale,type),7,linear).
    entity(scale,root,8).
    attribute((scale,channel),8,y).
    attribute((scale,type),8,linear).
    entity(scale,root,9).
    attribute((scale,channel),9,color).
    attribute((scale,type),9,linear).

    :- violation(_).
    """
    )

def shape_with_cardinality_gt_eight():
    b = hard.blocks["shape_with_cardinality_gt_eight"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    attribute((field,unique),0,5).
    entity(encoding,1,2).
    attribute((encoding,channel),2,shape).
    attribute((encoding,field),2,temperature).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    attribute((field,unique),0,10).
    entity(encoding,1,2).
    attribute((encoding,channel),2,shape).
    attribute((encoding,field),2,temperature).

    :- violation(_).
    """
    )

def color_with_cardinality_gt_twenty():
    b = hard.blocks["color_with_cardinality_gt_twenty"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    attribute((field,unique),0,5).
    entity(encoding,1,2).
    attribute((encoding,channel),2,color).
    attribute((encoding,field),2,temperature).
    entity(scale,root,3).
    attribute((scale,channel),3,color).
    attribute((scale,type),3,ordinal).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    attribute((field,unique),0,25).
    entity(encoding,1,2).
    attribute((encoding,channel),2,color).
    attribute((encoding,field),2,temperature).
    entity(scale,root,3).
    attribute((scale,channel),3,color).
    attribute((scale,type),3,ordinal).

    :- violation(_).
    """
    )

# === Type checks ===

def test_invalid_mark():
    b = hard.blocks["invalid_mark"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((mark,type),1,bar).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,root,1).
    attribute((mark,type),1,tickxx).

    :- violation(_).
    """
    )

def test_invalid_channel():
    b = hard.blocks["invalid_channel"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,xxx).

    :- violation(_).
    """
    )

def test_invalid_field_name():
    b = hard.blocks["invalid_field_name"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(mark,root,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,condition).

    :- violation(_).
    """
    )

def test_invalid_scale():
    b = hard.blocks["invalid_scale"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(scale,root,3).
    attribute((scale,channel),3,x).
    attribute((scale,type),3,linear).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(scale,root,3).
    attribute((scale,channel),3,x).
    attribute((scale,type),3,cosine).

    :- violation(_).
    """
    )

def test_invalid_aggregate():
    b = hard.blocks["invalid_aggregate"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,field),4,temperature).
    attribute((encoding,aggregate),4,mean).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,2,4).
    attribute((encoding,channel),4,y).
    attribute((encoding,field),4,temperature).
    attribute((encoding,aggregate),4,sum_mean).

    :- violation(_).
    """
    )

def test_invalid_bin():
    b = hard.blocks["invalid_bin"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    attribute((encoding,binning),2,30).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    attribute((encoding,binning),2).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,temperature).
    attribute((encoding,binning),2,-1).

    :- violation(_).
    """
    )

def test_invalid_field_type():
    b = hard.blocks["invalid_field_type"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,type),0,number).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,type),0,log).

    :- violation(_).
    """
    )

def test_invalid_task():
    b = hard.blocks["invalid_task"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    attribute(task,root,summary).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute(task,root,summary_task).

    :- violation(_).
    """
    )

def test_invalid_num_rows():
    b = hard.blocks["invalid_num_rows"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    attribute(number_rows,root,42).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    attribute(number_rows,root,0).

    :- violation(_).
    """
    )

def test_invalid_unique():
    b = hard.blocks["invalid_unique"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,unique),date,1461).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,unique),date,0).

    :- violation(_).
    """
    )

def test_invalid_extent_non_number_min():
    b = hard.blocks["invalid_extent_non_number_min"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,0).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,min),date,0).

    :- violation(_).
    """
    )

def test_invalid_extent_non_number_max():
    b = hard.blocks["invalid_extent_non_number_max"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,max),precipitation,55).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,max),date,55).

    :- violation(_).
    """
    )

def test_invalid_non_number_std():
    b = hard.blocks["invalid_non_number_std"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,std),precipitation,6).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,date).
    attribute((field,type),date,datetime).
    attribute((field,std),date,6).

    :- violation(_).
    """
    )

def test_invalid_std():
    b = hard.blocks["invalid_std"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,std),precipitation,6).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,std),precipitation,-10).

    :- violation(_).
    """
    )

def test_invalid_extent_order():
    b = hard.blocks["invalid_extent_order"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,0).
    attribute((field,max),precipitation,55).

    :- violation(_).
    """
    )

    assert is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,30).

    entity(field,root,precipitation2).
    attribute((field,type),precipitation2,number).
    attribute((field,max),precipitation2,20).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,min),precipitation,55).
    attribute((field,max),precipitation,0).

    :- violation(_).
    """
    )

def test_invalid_non_string_freq():
    b = hard.blocks["invalid_non_string_freq"]
    assert isinstance(b, Block)
    p = b.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,weather).
    attribute((field,type),weather,string).
    attribute((field,freq),weather,714).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,precipitation).
    attribute((field,type),precipitation,number).
    attribute((field,freq),precipitation,714).

    :- violation(_).
    """
    )

def test_encoding_field_same_name():
    b = hard.blocks["encoding_field_same_name"]
    assert isinstance(b, Block)
    p = b.program + define.program

    assert is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,temperature).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,x).

    :- violation(_).
    """
    )

    assert not is_satisfiable(
        p
        + """
    entity(field,root,0).
    attribute((field,name),0,detail).

    :- violation(_).
    """
    )


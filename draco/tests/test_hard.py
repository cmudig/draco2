from draco import dict_to_facts
from draco.asp_utils import Block
from draco.programs import hard, helpers
from draco.run import is_satisfiable, run_clingo


def list_violations(program: str):
    try:
        model = next(run_clingo(helpers.program + program, 1))

        return [
            symbol.arguments[0].name
            for symbol in model.answer_set
            if symbol.name == "violation"
        ]
    except StopIteration:
        return None


def no_violations(program: str):
    return is_satisfiable(helpers.program + program + ":- violation(_).")


def test_list_violations():
    assert list_violations(":- a. :- not a.") is None


def test_text_mark_without_text_channel():
    b = hard.blocks["text_mark_without_text_channel"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,text).
    """
    )

    # no encoding
    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,text).
    """
        )
        == ["text_mark_without_text_channel"]
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    """
        )
        == ["text_mark_without_text_channel"]
    )

    # text encoding for a different mark
    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,x).
    entity(encoding,m1,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,channel),e3,text).
    """
        )
        == ["text_mark_without_text_channel"]
    )


def test_text_channel_without_text_mark():
    b = hard.blocks["text_channel_without_text_mark"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((mark,type),m1,text).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((mark,type),m1,bar).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e1,text).
    """
        )
        == ["text_channel_without_text_mark"]
    )


def test_bin_and_aggregate():
    b = hard.blocks["bin_and_aggregate"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    entity(encoding,root,e2).
    attribute((encoding,channel),e2,y).
    attribute((encoding,aggregate),e2,count).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,root,e1).
    attribute((encoding,channel),e1,x).
    attribute((encoding,binning),e1,10).
    attribute((encoding,aggregate),e1,count).
    """
        )
        == ["bin_and_aggregate"]
    )


def test_no_encodings():
    b = hard.blocks["no_encodings"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    entity(encoding,1,2).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    entity(encoding,1,2).
    entity(mark,root,3).
    """
        )
        == ["no_encodings"]
    )


def test_repeat_channel():
    b = hard.blocks["repeat_channel"]
    assert isinstance(b, Block)

    # different channels
    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    entity(encoding,m0,e0).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,y).
    """
    )

    # no channel
    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    """
    )

    # different marks
    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    entity(mark,root,m1).
    entity(encoding,m0,e0).
    entity(encoding,m1,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,x).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,m0).
    entity(encoding,m0,e0).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e0,x).
    attribute((encoding,channel),e1,x).
    """
        )
        == ["repeat_channel"]
    )


def test_encoding_no_field_and_not_count():
    b = hard.blocks["encoding_no_field_and_not_count"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,field),1,temp).
    attribute((encoding,aggregate),1,mean).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,mean).
    """
        )
        == ["encoding_no_field_and_not_count"]
    )


def test_count_with_field():
    b = hard.blocks["count_with_field"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(encoding,root,1).
    attribute((encoding,aggregate),1,count).
    attribute((encoding,field),1,temp).
    """
        )
        == ["count_with_field"]
    )


def test_point_tick_bar_without_x_or_y():
    b = hard.blocks["point_tick_bar_without_x_or_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,x).
    entity(encoding,m0,e1).
    attribute((encoding,channel),e1,color).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,m0).
    attribute((mark,type),m0,tick).
    entity(encoding,m0,e0).
    attribute((encoding,channel),e0,color).
    """
        )
        == ["point_tick_bar_without_x_or_y"]
    )


def test_enc_type_valid():
    b = hard.blocks["enc_type_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,name),0,temperature).
    attribute((field,type),0,number).
    entity(mark,root,1).
    entity(encoding,1,3).
    entity(scale,root,5).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,name),0,temperature).
    attribute((field,type),0,string).
    entity(mark,0,1).
    entity(encoding,1,3).
    entity(scale,0,5).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
        )
        == ["enc_type_valid"]
    )

    # shared scale
    assert (
        list_violations(
            b.program
            + """
    attribute((field,name),0,temperature).
    attribute((field,type),0,string).
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,5).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,temperature).
    attribute((scale,channel),5,x).
    attribute((scale,type),5,linear).
    """
        )
        == ["enc_type_valid"]
    )


def test_bin_q_o():
    b = hard.blocks["bin_q_o"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,binning),2,10).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
        )
        == ["bin_q_o"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,4).
    attribute((encoding,channel),3,x).
    attribute((encoding,binning),3,10).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
        )
        == ["bin_q_o"]
    )


def test_log_non_positive():
    b = hard.blocks["log_non_positive"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).

    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,field),2,precipitation).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,log).
    """
        )
        == ["log_non_positive"]
    )


def test_aggregate_o_valid():
    b = hard.blocks["aggregate_o_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,median).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,mean).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).
    """
        )
        == ["aggregate_o_valid"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,4).
    attribute((encoding,channel),3,x).
    attribute((encoding,aggregate),3,mean).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).
    """
        )
        == ["aggregate_o_valid"]
    )


def test_aggregate_t_valid():
    b = hard.blocks["aggregate_t_valid"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,name),0,time).
    attribute((field,type),0,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,min).
    """
    )

    assert no_violations(
        b.program
        + """
    attribute((field,name),0,time).
    attribute((field,type),0,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,max).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,name),0,time).
    attribute((field,type),0,datetime).
    attribute((encoding,channel),3,x).
    attribute((encoding,field),3,time).
    attribute((encoding,aggregate),3,median).
    """
        )
        == ["aggregate_t_valid"]
    )


def test_aggregate_nominal():
    b = hard.blocks["aggregate_nominal"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,ordinal).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
        )
        == ["aggregate_nominal"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(view,0,1).
    entity(mark,1,2).
    entity(encoding,2,3).
    entity(scale,0,4).
    attribute((encoding,channel),3,x).
    attribute((encoding,aggregate),3,min).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
        )
        == ["aggregate_nominal"]
    )


def test_aggregate_detail():
    b = hard.blocks["aggregate_detail"]
    assert isinstance(b, Block)

    assert (
        list_violations(
            b.program
            + """
    attribute((encoding,channel),2,detail).
    attribute((encoding,aggregate),2,min).
    """
        )
        == ["aggregate_detail"]
    )


def test_count_q_without_field():
    b = hard.blocks["count_q_without_field"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    attribute((scale,channel),4,y).
    attribute((scale,type),4,categorical).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(encoding,1,2).
    attribute((encoding,field),2,temp).
    attribute((encoding,aggregate),2,count).
    """
        )
        == ["count_q_without_field"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(encoding,1,2).
    entity(scale,0,4).
    attribute((encoding,channel),2,x).
    attribute((encoding,aggregate),2,count).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,categorical).
    """
        )
        == ["count_q_without_field"]
    )


def test_shape_discrete_non_ordered():
    b = hard.blocks["shape_discrete_non_ordered"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((scale,channel),4,shape).
    attribute((scale,type),4,categorical).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((scale,channel),4,shape).
    attribute((scale,type),4,ordinal).
    """
        )
        == ["shape_discrete_non_ordered"]
    )


def test_detail_non_ordered():
    b = hard.blocks["detail_non_ordered"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((scale,channel),4,detail).
    attribute((scale,type),4,categorical).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((scale,channel),4,detail).
    attribute((scale,type),4,ordinal).
    """
        )
        == ["detail_non_ordered"]
    )


def test_size_nominal():
    b = hard.blocks["size_nominal"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((scale,channel),4,size).
    attribute((scale,type),4,linear).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((scale,channel),4,size).
    attribute((scale,type),4,categorical).
    """
        )
        == ["size_nominal"]
    )


def test_size_negative():
    b = hard.blocks["size_negative"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    attribute((field,min),precipitation,0).
    attribute((field,max),precipitation,55).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    attribute((encoding,field),1,precipitation).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    attribute((field,min),precipitation,-10).
    attribute((field,max),precipitation,55).
    entity(encoding,0,1).
    attribute((encoding,channel),1,size).
    attribute((encoding,field),1,precipitation).
    """
        )
        == ["size_negative"]
    )


def test_line_area_without_x_y():
    b = hard.blocks["line_area_without_x_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(encoding,1,3).
    attribute((encoding,channel),3,y).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    attribute((mark,type),1,line).
    entity(encoding,1,2).
    attribute((encoding,channel),2,y).
    """
        )
        == ["line_area_without_x_y"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    """
        )
        == ["line_area_without_x_y"]
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,root,1).
    attribute((mark,type),1,area).
    entity(encoding,1,2).
    """
        )
        == ["line_area_without_x_y"]
    )


def test_line_area_with_discrete():
    b = hard.blocks["line_area_with_discrete"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(scale,0,2).
    entity(scale,0,3).
    attribute((mark,type),1,line).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,linear).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,linear).
    """
    )

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    entity(scale,0,2).
    entity(scale,0,3).
    attribute((mark,type),1,line).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,categorical).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,linear).
    """
    )

    assert (
        list_violations(
            b.program
            + """
    entity(mark,0,1).
    entity(scale,0,2).
    entity(scale,0,3).
    attribute((mark,type),1,line).
    attribute((scale,channel),2,x).
    attribute((scale,type),2,categorical).
    attribute((scale,channel),3,y).
    attribute((scale,type),3,ordinal).
    """
        )
        == ["line_area_with_discrete"]
    )


def test_bar_tick_continuous_x_y():
    b = hard.blocks["bar_tick_continuous_x_y"]
    assert isinstance(b, Block)

    assert no_violations(
        b.program
        + """
    entity(mark,0,1).
    attribute((mark,type),1,tick).
    entity(encoding,1,2).
    attribute((encoding,channel),2,x).
    entity(scale,0,4).
    attribute((scale,channel),4,x).
    attribute((scale,type),4,linear).
    """
    )

    assert no_violations(
        b.program
        + ("\n").join(
            dict_to_facts(
                {
                    "mark": [
                        {
                            "type": "tick",
                            "encoding": [
                                {"channel": "x", "field": "temperature"},
                                {"channel": "y", "field": "wind"},
                            ],
                        }
                    ],
                    "scale": [
                        {"channel": "x", "type": "linear"},
                        {"channel": "y", "type": "categorical"},
                    ],
                }
            )
        )
    )

    # multiple views
    assert (
        list_violations(
            b.program
            + ("\n").join(
                dict_to_facts(
                    {
                        "view": [
                            {
                                "mark": [
                                    {
                                        "type": "tick",
                                        "encoding": [
                                            {"channel": "y", "field": "temperature"}
                                        ],
                                    }
                                ],
                                "scale": [{"channel": "y", "type": "linear"}],
                            },
                            {
                                "mark": [
                                    {
                                        "type": "bar",
                                        "encoding": [
                                            {"channel": "x", "field": "temperature"},
                                            {"channel": "y", "aggregate": "count"},
                                        ],
                                    }
                                ],
                                "scale": [
                                    {"channel": "x", "type": "linear"},
                                    {"channel": "y", "type": "linear"},
                                ],
                            },
                        ]
                    }
                )
            )
        )
        == ["bar_tick_continuous_x_y"]
    )

    # multiple views with one shared-scale
    assert no_violations(
        b.program
        + ("\n").join(
            dict_to_facts(
                {
                    "view": [
                        {
                            "mark": [
                                {
                                    "type": "tick",
                                    "encoding": [
                                        {"channel": "y", "field": "temperature"}
                                    ],
                                }
                            ]
                        },
                        {
                            "mark": [
                                {
                                    "type": "bar",
                                    "encoding": [
                                        {"channel": "x", "field": "temperature"},
                                        {"channel": "y", "aggregate": "count"},
                                    ],
                                }
                            ],
                            "scale": [{"channel": "x", "type": "ordinal"}],
                        },
                    ],
                    "scale": [{"channel": "y", "type": "linear"}],
                }
            )
        )
    )

    assert (
        list_violations(
            b.program
            + ("\n").join(
                dict_to_facts(
                    {
                        "view": [
                            {
                                "mark": [
                                    {
                                        "type": "tick",
                                        "encoding": [
                                            {"channel": "y", "field": "temperature"}
                                        ],
                                    }
                                ]
                            },
                            {
                                "mark": [
                                    {
                                        "type": "bar",
                                        "encoding": [
                                            {"channel": "x", "field": "temperature"},
                                            {"channel": "y", "aggregate": "count"},
                                        ],
                                    }
                                ],
                                "scale": [{"channel": "x", "type": "linear"}],
                            },
                        ],
                        "scale": [{"channel": "y", "type": "linear"}],
                    }
                )
            )
        )
        == ["bar_tick_continuous_x_y"]
    )
